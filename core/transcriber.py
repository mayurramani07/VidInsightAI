import os
import time
import requests
from pydub import AudioSegment
from groq import Groq

from utils.metrics import metrics  

# Sarvam's sync STT-translate API rejects audio longer than 30s.
SARVAM_PIECE_SECONDS = 25

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_STT_TRANSLATE_URL = "https://api.sarvam.ai/speech-to-text-translate"
SARVAM_MODEL = os.getenv("SARVAM_STT_MODEL", "saaras:v2.5")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_WHISPER_MODEL = os.getenv("GROQ_WHISPER_MODEL", "whisper-large-v3-turbo")


def transcribe_chunk_groq(chunk_path: str) -> str:
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set in environment / .env")

    client = Groq(api_key=GROQ_API_KEY)

    start = time.time()  # 🆕 metric timing

    with open(chunk_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=(os.path.basename(chunk_path), audio_file.read()),
            model=GROQ_WHISPER_MODEL,
            response_format="json",
            language="en",
        )

    metrics.inc("whisper_calls")
    metrics.time_end("whisper_latency", start)

    return transcription.text

def _send_to_sarvam(piece_path: str) -> str:
    headers = {"api-subscription-key": SARVAM_API_KEY}

    max_retries = 5

    for attempt in range(max_retries):
        with open(piece_path, "rb") as f:
            files = {"file": (os.path.basename(piece_path), f, "audio/wav")}

            data = {
                "model": SARVAM_MODEL,
                "with_diarization": "false"
            }

            response = requests.post(
                SARVAM_STT_TRANSLATE_URL,
                headers=headers,
                files=files,
                data=data,
                timeout=120,
            )

        if response.ok:
            metrics.inc("sarvam_calls")  # 🆕
            return response.json().get("transcript", "")

        if response.status_code == 429:
            wait_time = 10 * (attempt + 1)
            print("\nSarvam rate limit hit: 429")
            print(f"Waiting {wait_time} seconds before retry...")
            time.sleep(wait_time)
            continue

        response.raise_for_status()

    raise RuntimeError("Sarvam rate limit exceeded even after retries.")


def transcribe_chunk_sarvam(chunk_path: str) -> str:
    if not SARVAM_API_KEY:
        raise RuntimeError("SARVAM_API_KEY is not set in environment / .env")

    audio = AudioSegment.from_wav(chunk_path)
    piece_ms = SARVAM_PIECE_SECONDS * 1000

    full_text = ""

    total_pieces = (len(audio) + piece_ms - 1) // piece_ms

    for i, start in enumerate(range(0, len(audio), piece_ms)):
        piece = audio[start: start + piece_ms]
        piece_path = f"{chunk_path}_sv_{i}.wav"

        piece.export(piece_path, format="wav")

        try:
            print(f"  → Sarvam piece {i + 1}/{total_pieces} ...", flush=True)

            start_t = time.time()  # 🆕
            transcript = _send_to_sarvam(piece_path)
            metrics.time_end("sarvam_latency", start_t)  # 🆕

            full_text += transcript + " "

            time.sleep(3)

        finally:
            if os.path.exists(piece_path):
                os.remove(piece_path)

    return full_text.strip()


def transcribe_chunk(chunk_path: str, language: str = "english") -> str:
    if language.lower() == "hinglish":
        return transcribe_chunk_sarvam(chunk_path)

    return transcribe_chunk_groq(chunk_path)


def transcribe_all(chunks: list, language: str = "english") -> str:
    full_transcript = ""

    engine = "Sarvam AI" if language.lower() == "hinglish" else "Groq Whisper API"
    print(f"Using {engine} for transcription.", flush=True)

    for i, chunk in enumerate(chunks):
        print(f"Transcribing chunk {i + 1}/{len(chunks)}...", flush=True)

        text = transcribe_chunk(chunk, language=language)
        full_transcript += text + " "

    return full_transcript.strip()