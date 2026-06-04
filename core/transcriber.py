# import whisper
# import os
# import requests
# import time
# from pydub import AudioSegment

# # Sarvam's sync STT-translate API rejects audio longer than 30s.
# # We slice each chunk into 25s pieces before sending.
# SARVAM_PIECE_SECONDS = 25

# WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

# SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
# SARVAM_STT_TRANSLATE_URL = "https://api.sarvam.ai/speech-to-text-translate"
# SARVAM_MODEL = os.getenv("SARVAM_STT_MODEL", "saaras:v2.5")

# _model = None


# def load_model():
#     global _model

#     if _model is None:
#         print(f"Loading Whisper model: {WHISPER_MODEL} ...")
#         _model = whisper.load_model(WHISPER_MODEL)
#         print("Whisper model loaded.")

#     return _model


# def transcribe_chunk_whisper(chunk_path: str) -> str:
#     model = load_model()

#     result = model.transcribe(chunk_path, task="transcribe")
#     return result["text"]


# def _send_to_sarvam(piece_path: str) -> str:
#     """
#     Send one ≤30s WAV file to Sarvam and return the English transcript.
#     Handles 429 rate-limit errors using retry + backoff.
#     """
#     headers = {"api-subscription-key": SARVAM_API_KEY}

#     max_retries = 5

#     for attempt in range(max_retries):
#         with open(piece_path, "rb") as f:
#             files = {"file": (os.path.basename(piece_path), f, "audio/wav")}

#             data = {
#                 "model": SARVAM_MODEL,
#                 "with_diarization": "false"
#             }

#             response = requests.post(
#                 SARVAM_STT_TRANSLATE_URL,
#                 headers=headers,
#                 files=files,
#                 data=data,
#                 timeout=120,
#             )

#         if response.ok:
#             return response.json().get("transcript", "")

#         if response.status_code == 429:
#             wait_time = 10 * (attempt + 1)

#             print(f"\nSarvam rate limit hit: 429")
#             print(f"Waiting {wait_time} seconds before retry...")
#             print(f"Response body: {response.text}\n")

#             time.sleep(wait_time)
#             continue

#         print(f"\nSarvam returned {response.status_code}")
#         print(f"Response body: {response.text}\n")
#         response.raise_for_status()

#     raise RuntimeError("Sarvam rate limit exceeded even after retries.")


# def transcribe_chunk_sarvam(chunk_path: str) -> str:
#     """
#     Sarvam sync API only accepts ≤30s audio.
#     We split this chunk into 25-second pieces, send each separately,
#     and join the transcripts.
#     """
#     if not SARVAM_API_KEY:
#         raise RuntimeError("SARVAM_API_KEY is not set in environment / .env")

#     audio = AudioSegment.from_wav(chunk_path)
#     piece_ms = SARVAM_PIECE_SECONDS * 1000

#     full_text = ""
#     total_pieces = (len(audio) + piece_ms - 1) // piece_ms

#     for i, start in enumerate(range(0, len(audio), piece_ms)):
#         piece = audio[start: start + piece_ms]
#         piece_path = f"{chunk_path}_sv_{i}.wav"

#         piece.export(piece_path, format="wav")

#         try:
#             print(f"  → Sarvam piece {i + 1}/{total_pieces} ...")

#             transcript = _send_to_sarvam(piece_path)
#             full_text += transcript + " "

#             # Small delay to avoid hitting Sarvam rate limit
#             time.sleep(3)

#         finally:
#             if os.path.exists(piece_path):
#                 os.remove(piece_path)

#     return full_text.strip()


# def transcribe_chunk(chunk_path: str, language: str = "english") -> str:
#     """
#     Route one chunk to Whisper or Sarvam depending on language choice.

#     - english  → Whisper local model
#     - hinglish → Sarvam STT translate API
#     """
#     if language.lower() == "hinglish":
#         return transcribe_chunk_sarvam(chunk_path)

#     return transcribe_chunk_whisper(chunk_path)


# def transcribe_all(chunks: list, language: str = "english") -> str:
#     full_transcript = ""

#     engine = "Sarvam AI" if language.lower() == "hinglish" else "Whisper"
#     print(f"Using {engine} for transcription.")

#     for i, chunk in enumerate(chunks):
#         print(f"Transcribing chunk {i + 1}/{len(chunks)}...")

#         text = transcribe_chunk(chunk, language=language)
#         full_transcript += text + " "

#     print("Transcription complete.")

#     return full_transcript.strip()

import os
import time
import requests
from pydub import AudioSegment
from groq import Groq

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

    with open(chunk_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=(os.path.basename(chunk_path), audio_file.read()),
            model=GROQ_WHISPER_MODEL,
            response_format="json",
            language="en",
        )

    return transcription.text


def _send_to_sarvam(piece_path: str) -> str:
    """
    Send one ≤30s WAV file to Sarvam and return the English transcript.
    Handles 429 rate-limit errors using retry + backoff.
    """
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
            return response.json().get("transcript", "")

        if response.status_code == 429:
            wait_time = 10 * (attempt + 1)

            print("\nSarvam rate limit hit: 429")
            print(f"Waiting {wait_time} seconds before retry...")
            print(f"Response body: {response.text}\n")

            time.sleep(wait_time)
            continue

        print(f"\nSarvam returned {response.status_code}")
        print(f"Response body: {response.text}\n")
        response.raise_for_status()

    raise RuntimeError("Sarvam rate limit exceeded even after retries.")


def transcribe_chunk_sarvam(chunk_path: str) -> str:
    """
    Sarvam sync API only accepts ≤30s audio.
    We split this chunk into 25-second pieces, send each separately,
    and join the transcripts.
    """
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

            transcript = _send_to_sarvam(piece_path)
            full_text += transcript + " "

            time.sleep(3)

        finally:
            if os.path.exists(piece_path):
                os.remove(piece_path)

    return full_text.strip()


def transcribe_chunk(chunk_path: str, language: str = "english") -> str:
    """
    Route one chunk to Groq Whisper or Sarvam depending on language choice.

    - english  → Groq Whisper API
    - hinglish → Sarvam STT translate API
    """
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

    print("Transcription complete.", flush=True)

    return full_transcript.strip()