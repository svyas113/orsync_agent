#!/usr/bin/env python3
"""Serve the Or-sync visitor agent with Flux-name scrubbing on all API JSON replies."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
WF = ROOT / "orsync_visitor"

sys.path.insert(0, str(REPO))
sys.path.insert(0, str(WF))

from application.sanitize import scrub  # noqa: E402


def _scrub_obj(obj):
    if isinstance(obj, str):
        return scrub(obj)
    if isinstance(obj, list):
        return [_scrub_obj(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _scrub_obj(v) for k, v in obj.items()}
    return obj


class ScrubFluxMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        content_type = response.headers.get("content-type", "")
        if "application/json" not in content_type:
            return response
        body = b""
        async for chunk in response.body_iterator:
            body += chunk
        try:
            data = json.loads(body.decode("utf-8"))
            data = _scrub_obj(data)
            new_body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        except Exception:
            new_body = body
        headers = dict(response.headers)
        headers.pop("content-length", None)
        return Response(
            content=new_body,
            status_code=response.status_code,
            headers=headers,
            media_type=response.media_type,
        )


def main() -> None:
    port = os.environ.get("PORT", "8003")
    argv = [
        "fastapi_fastworkflow",
        "--workflow_path",
        str(WF),
        "--env_file_path",
        str(WF / "fastworkflow.env"),
        "--passwords_file_path",
        str(WF / "fastworkflow.passwords.env"),
        "--startup_action",
        str(WF / "startup_action.json"),
        "--host",
        "0.0.0.0",
        "--port",
        str(port),
    ]
    sys.argv = argv

    import fastapi_fastworkflow.__main__ as fw_main

    fw_main.app.add_middleware(ScrubFluxMiddleware)
    fw_main.main()


if __name__ == "__main__":
    main()
