"""
Optimized FastAPI backend for AI Bioinformatics Assistant.
Includes caching, request limiting, and memory optimization.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
import sys
from functools import lru_cache
import hashlib

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.parser import parse_sequence_file
from utils.analysis import analyze_multiple_sequences, detect_open_reading_frames
from utils.ai_utils import chat_with_bioinformatics_ai

app = FastAPI(title="AI Bioinformatics Assistant API", version="1.0.0")

origins = [
    "http://localhost",
    "http://localhost:8501",
    "http://127.0.0.1:8501",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    query: str
    chat_history: Optional[List[Dict[str, str]]] = None
    sequence_context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    response: str
    error: bool = False
    message: Optional[str] = None
    model: Optional[str] = None


class SequenceAnalysisRequest(BaseModel):
    content: str
    file_format: str
    detect_orfs: bool = False


class SequenceAnalysisResponse(BaseModel):
    success: bool
    analysis: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    orfs: Optional[List[Dict[str, Any]]] = None


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "running",
        "service": "AI Bioinformatics Assistant API",
        "version": "1.0.0"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for bioinformatics questions.

    Request body:
    - query: User's question
    - chat_history: Optional previous messages
    - sequence_context: Optional sequence analysis results

    Returns:
    - response: AI's answer
    - error: Whether there was an error
    - message: Error message if any
    - model: Model used
    """
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=400,
            detail="OPENROUTER_API_KEY environment variable not set"
        )

    if not request.query or not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty"
        )

    try:
        result = chat_with_bioinformatics_ai(
            api_key=api_key,
            user_query=request.query,
            chat_history=request.chat_history or [],
            sequence_context=request.sequence_context
        )

        if result.get("error"):
            return ChatResponse(
                response="",
                error=True,
                message=result.get("message", "Unknown error")
            )

        return ChatResponse(
            response=result.get("response", ""),
            error=False,
            model=result.get("model")
        )
    except Exception as e:
        import traceback
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        print(f"Chat error: {error_msg}")
        raise HTTPException(
            status_code=500,
            detail=f"Chat error: {str(e)}"
        )


@app.post("/analyze", response_model=SequenceAnalysisResponse)
async def analyze_sequences(request: SequenceAnalysisRequest):
    """
    Analyze biological sequences with optimized memory usage.

    Request body:
    - content: File content as string (max 10MB)
    - file_format: 'fasta', 'fa', 'fna', 'fastq', or 'fq'
    - detect_orfs: Whether to detect open reading frames

    Returns:
    - success: Whether analysis was successful
    - analysis: Analysis results
    - error: Error message if any
    - orfs: Detected ORFs if requested (limited to 1000)
    """
    # Check content size (10MB limit)
    max_size_bytes = 10 * 1024 * 1024
    if len(request.content) > max_size_bytes:
        return SequenceAnalysisResponse(
            success=False,
            error=f"File too large. Maximum size: 10MB. Received: {len(request.content) / (1024*1024):.1f}MB"
        )

    if not request.content or not request.content.strip():
        return SequenceAnalysisResponse(
            success=False,
            error="File content cannot be empty"
        )

    try:
        sequences, parse_error = parse_sequence_file(request.content, request.file_format)

        if parse_error:
            return SequenceAnalysisResponse(
                success=False,
                error=parse_error
            )

        analysis = analyze_multiple_sequences(sequences, limit=10000)

        orfs = None
        if request.detect_orfs and sequences:
            try:
                orfs = []
                orf_count = 0
                max_total_orfs = 1000

                for seq in sequences[:100]:
                    seq_orfs = detect_open_reading_frames(seq['sequence'], max_orfs=100)
                    if seq_orfs:
                        for orf in seq_orfs:
                            if orf_count >= max_total_orfs:
                                break
                            orfs.append({
                                "sequence_header": seq['header'],
                                **orf
                            })
                            orf_count += 1
                    if orf_count >= max_total_orfs:
                        break
            except Exception as e:
                pass

        return SequenceAnalysisResponse(
            success=True,
            analysis=analysis,
            orfs=orfs
        )

    except MemoryError:
        return SequenceAnalysisResponse(
            success=False,
            error="Insufficient memory to process file. Please try a smaller file."
        )
    except Exception as e:
        return SequenceAnalysisResponse(
            success=False,
            error=f"Analysis error: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Detailed health check."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    return {
        "status": "healthy",
        "api_key_configured": bool(api_key),
        "endpoints": {
            "chat": "/chat",
            "analyze": "/analyze",
            "health": "/health"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
