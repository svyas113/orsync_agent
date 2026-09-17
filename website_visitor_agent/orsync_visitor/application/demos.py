"""Public demo agent catalog and random selection."""

from __future__ import annotations

import os
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class DemoAgent:
    key: str
    name: str
    pitch: str
    env_url_key: str

    @property
    def url(self) -> str | None:
        value = (os.environ.get(self.env_url_key) or "").strip()
        return value or None


DEMO_AGENTS: tuple[DemoAgent, ...] = (
    DemoAgent(
        key="spyran",
        name="Spyran",
        pitch=(
            "Spyran is a retail support demo: search products, browse categories, "
            "get product details, and manage a cart (packaged foods / masalas catalog)."
        ),
        env_url_key="DEMO_SPYRAN_URL",
    ),
    DemoAgent(
        key="zebrata",
        name="Zebrata",
        pitch=(
            "Zebrata is a jewellery & home décor demo with catalog/cart flows "
            "plus virtual try-on from a selfie."
        ),
        env_url_key="DEMO_ZEBRATA_URL",
    ),
    DemoAgent(
        key="rvd",
        name="RVD Jewels",
        pitch=(
            "RVD Jewels is a jewellery retail demo with catalog/cart flows "
            "plus virtual try-on, using an RVD Jewels–style catalog."
        ),
        env_url_key="DEMO_RVD_URL",
    ),
)


def list_demos() -> list[DemoAgent]:
    return list(DEMO_AGENTS)


def find_demo(name_or_key: str) -> DemoAgent | None:
    needle = (name_or_key or "").strip().lower()
    if not needle:
        return None
    aliases = {
        "spyran": "spyran",
        "spy ran": "spyran",
        "retail": "spyran",
        "zebrata": "zebrata",
        "zebra": "zebrata",
        "jewellery try on": "zebrata",
        "rvd": "rvd",
        "rvd jewels": "rvd",
        "rvdjewels": "rvd",
        "jewels": "rvd",
    }
    key = aliases.get(needle)
    if key is None:
        for demo in DEMO_AGENTS:
            if needle in demo.key or needle in demo.name.lower():
                key = demo.key
                break
    if key is None:
        return None
    for demo in DEMO_AGENTS:
        if demo.key == key:
            return demo
    return None


def pick_random_demo() -> DemoAgent:
    return random.choice(DEMO_AGENTS)


def format_demo_handoff(demo: DemoAgent) -> str:
    url = demo.url
    if url:
        return (
            f"{demo.name}: {demo.pitch}\n\n"
            f"Open the demo here (new tab): {url}"
        )
    return (
        f"{demo.name}: {demo.pitch}\n\n"
        "A public link for this demo is not configured yet. "
        "I can request a private walkthrough for you — share your name, email, "
        "and what you'd like to see."
    )


def format_all_demos() -> str:
    lines = []
    for demo in DEMO_AGENTS:
        status = demo.url or "(link not configured — ask for a private demo)"
        lines.append(f"- {demo.name}: {demo.pitch}\n  Link: {status}")
    return (
        "Here are our public demo agents:\n\n"
        + "\n\n".join(lines)
        + "\n\nSay “random demo” to open one at random, or name Spyran, Zebrata, or RVD Jewels."
    )
