from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://vidinsightai.vercel.app/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_chain_store = {
    "rag_chain": None
}


class AnalyzeRequest(BaseModel):
    source: str
    language: str = "english"


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "VidInsight AI backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/api/analyze")
def analyze_video(request: AnalyzeRequest):
    try:
        from utils.audio_processor import process_input
        from core.transcriber import transcribe_all
        from core.summarize import summarize, generate_title
        from core.extractor import (
            extract_action_items,
            extract_key_decisions,
            extract_questions,
        )
        from core.rag_engine import build_rag_chain

        print("Starting AI Video Assistant API pipeline")

        chunks = process_input(request.source)

        transcript = transcribe_all(chunks, request.language)

        title = generate_title(transcript)

        summary = summarize(transcript)

        action_items = extract_action_items(transcript)

        decisions = extract_key_decisions(transcript)

        questions = extract_questions(transcript)

        rag_chain = build_rag_chain(transcript)

        rag_chain_store["rag_chain"] = rag_chain

        return {
            "title": title,
            "transcript": transcript,
            "summary": summary,
            "action_items": action_items,
            "key_decisions": decisions,
            "open_questions": questions,
        }

    except Exception as e:
        print("API error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
def chat_with_video(request: ChatRequest):
    try:
        from core.rag_engine import ask_question

        rag_chain = rag_chain_store.get("rag_chain")

        if rag_chain is None:
            raise HTTPException(
                status_code=400,
                detail="Please analyze a video first before asking questions.",
            )

        answer = ask_question(rag_chain, request.question)

        return {
            "answer": answer
        }

    except HTTPException:
        raise

    except Exception as e:
        print("Chat error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))