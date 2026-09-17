#!/usr/bin/env python3
"""Smoke tests for Or-sync visitor agent application logic (no API keys required)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from application.session import VisitorSession


def main() -> None:
    session = VisitorSession()

    caps = session.what_can_you_do()
    assert "demo" in caps.lower()
    assert "flux" not in caps.lower()
    print("what_can_you_do: ok")

    explain = session.explain_ai_agents()
    assert "ai agent" in explain.lower()
    assert "flux" not in explain.lower()
    print("explain_ai_agents: ok")

    about = session.about_orsync()
    assert "2026" in about and "fastWorkflow" in about
    assert "flux" not in about.lower()
    print("about_orsync: ok")

    services = session.list_services()
    assert "Custom Agent" in services
    print("list_services: ok")

    listed = session.open_demo_agent()
    assert "Spyran" in listed and "Zebrata" in listed and "RVD" in listed
    assert "flux" not in listed.lower()
    print("open_demo_agent list: ok")

    os.environ["DEMO_SPYRAN_URL"] = "https://example.com/spyran"
    pick = session.open_demo_agent(random_pick=True)
    assert "Spyran" in pick or "Zebrata" in pick or "RVD" in pick
    print("open_demo_agent random: ok")

    named = session.open_demo_agent(agent_name="Spyran")
    assert "Spyran" in named and "example.com/spyran" in named
    print("open_demo_agent Spyran: ok")

    # SMTP may be configured now — just ensure call returns a result object
    result = session.request_demo(
        name="Ada Lovelace",
        email="ada@example.com",
        company="Analytical Engines",
        message="Want a custom retail agent walkthrough",
        interest="custom agent",
    )
    assert hasattr(result, "ok") and hasattr(result, "detail")
    assert "flux" not in result.detail.lower()
    print("request_demo: ok ->", result.ok, result.detail[:80])

    print("All smoke tests passed.")


if __name__ == "__main__":
    main()
