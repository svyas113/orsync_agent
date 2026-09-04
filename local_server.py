"""Local inbox server: serves chat UI and proxies to FastWorkflow FastAPI."""

from __future__ import annotations

import json
import os
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).resolve().parent
CHAT_UI_DIR = PROJECT_ROOT / "chat_ui"
FASTWORKFLOW_BASE = os.getenv("FASTWORKFLOW_BASE_URL", "http://127.0.0.1:8000")

app = FastAPI(title="Or-sync Local Inbox")
app.mount("/static", StaticFiles(directory=CHAT_UI_DIR / "static"), name="static")


class InitializeRequest(BaseModel):
    channel_id: str
    user_id: str
    stream_format: str = "ndjson"


class ChatRequest(BaseModel):
    user_query: str
    timeout_seconds: int = 90


@app.get("/", response_class=HTMLResponse)
async def index() -> FileResponse:
    return FileResponse(CHAT_UI_DIR / "index.html")


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "fastworkflow_base": FASTWORKFLOW_BASE}


@app.post("/api/initialize")
async def initialize(payload: InitializeRequest) -> dict:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{FASTWORKFLOW_BASE}/initialize",
            json=payload.model_dump(),
        )
    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()


@app.post("/api/refresh")
async def refresh(request: Request) -> dict:
    auth = request.headers.get("Authorization", "")
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{FASTWORKFLOW_BASE}/refresh_token",
            headers={"Authorization": auth},
        )
    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()


@app.post("/api/new_conversation")
async def new_conversation(request: Request) -> dict:
    auth = request.headers.get("Authorization", "")
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{FASTWORKFLOW_BASE}/new_conversation",
            headers={"Authorization": auth},
        )
    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()


@app.post("/api/chat")
async def chat(payload: ChatRequest, request: Request):
    auth = request.headers.get("Authorization", "")

    async def stream_proxy():
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST",
                f"{FASTWORKFLOW_BASE}/invoke_agent_stream",
                headers={"Authorization": auth, "Content-Type": "application/json"},
                json=payload.model_dump(),
            ) as response:
                if response.status_code >= 400:
                    detail = (await response.aread()).decode("utf-8", errors="replace")
                    yield (
                        json.dumps({"type": "error", "data": {"detail": detail}}) + "\n"
                    ).encode()
                    return
                async for chunk in response.aiter_bytes():
                    yield chunk

    return StreamingResponse(stream_proxy(), media_type="application/x-ndjson")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "local_server:app",
        host="0.0.0.0",
        port=int(os.getenv("INBOX_PORT", "8765")),
        reload=False,
    )
