from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from dotenv import load_dotenv

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import summarize, generate_title
from core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions,
)
from core.rag_engine import build_rag_chain, ask_question
from utils.metrics import metrics

import time

load_dotenv()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://vidinsightai.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


rag_chain_store = {"rag_chain": None}


class AnalyzeRequest(BaseModel):
    source: str
    language: str = "english"

class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "VidInsight AI backend is running"}


@app.post("/api/analyze")
def analyze_video(request: AnalyzeRequest):
    start_time = time.time()

    try:
        print("Starting AI Video Assistant API pipeline")

      
        metrics.inc("videos_processed")
        metrics.inc("api_calls")

        
        chunks = process_input(request.source)

       
        transcript = transcribe_all(chunks, request.language)

        metrics.inc("total_audio_seconds", len(chunks) * 25)


        title = generate_title(transcript)
        summary = summarize(transcript)

        action_items = extract_action_items(transcript)
        decisions = extract_key_decisions(transcript)
        questions = extract_questions(transcript)

        
        rag_chain = build_rag_chain(transcript)
        rag_chain_store["rag_chain"] = rag_chain

       
        processing_time = time.time() - start_time

      
        metrics.time_end("analyze_latency", start_time)

        return {
            "title": title,
            "transcript": transcript,
            "summary": summary,
            "action_items": action_items,
            "key_decisions": decisions,
            "open_questions": questions,
            "processing_time": processing_time,
        }

    except Exception as e:
        metrics.inc("errors")
        print("API error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
def chat_with_video(request: ChatRequest):
    try:
        rag_chain = rag_chain_store.get("rag_chain")

        if rag_chain is None:
            raise HTTPException(
                status_code=400,
                detail="Please analyze a video first before asking questions.",
            )

        metrics.inc("chat_queries")

        answer = ask_question(rag_chain, request.question)

        return {"answer": answer}

    except HTTPException:
        raise

    except Exception as e:
        metrics.inc("errors")
        print("Chat error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metrics")
def get_metrics():
    try:
        return {
            "counters": dict(metrics.data),
            "avg_timings": {
                k: (sum(v) / len(v) if v else 0)
                for k, v in metrics.timings.items()
            },
            "live": {
                "videos_processed": metrics.data.get("videos_processed", 0),
                "api_calls": metrics.data.get("api_calls", 0),
                "chat_queries": metrics.data.get("chat_queries", 0),
                "errors": metrics.data.get("errors", 0),
                "total_audio_seconds": metrics.data.get("total_audio_seconds", 0),
            },
        }

    except Exception as e:
        return {"error": str(e)}