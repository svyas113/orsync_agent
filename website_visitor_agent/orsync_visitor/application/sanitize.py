"""Strip banned product names and markdown from visitor-facing text."""

from __future__ import annotations

import re

_BANNED = re.compile(r"\bflux(?:\s*designer)?\b", re.IGNORECASE)

_SAFE_REPLY = (
    "I can help with Or-sync company info, our services, "
    "public demos (Spyran, Zebrata, RVD Jewels), or a private demo request. "
    "What would you like to explore?"
)

_MD_LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
_BOLD = re.compile(r"\*\*(.+?)\*\*|__(.+?)__")
_ITALIC = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)|(?<!_)_(?!_)(.+?)(?<!_)_(?!_)")
_CODE = re.compile(r"`([^`]*)`")
_HEADING = re.compile(r"(?m)^#{1,6}\s+")
_MULTI_NL = re.compile(r"\n{3,}")


def to_plain_text(text: str) -> str:
    """Convert common markdown markers into browser-friendly plain text."""
    if not text:
        return text

    def _link_repl(match: re.Match[str]) -> str:
        label = (match.group(1) or "").strip()
        url = (match.group(2) or "").strip()
        if not url:
            return label
        if not label or label == url or label.startswith(url) or url.startswith(label):
            return url
        return f"{label}: {url}"

    out = _MD_LINK.sub(_link_repl, text)
    out = _BOLD.sub(lambda m: m.group(1) or m.group(2) or "", out)
    out = _ITALIC.sub(lambda m: m.group(1) or m.group(2) or "", out)
    out = _CODE.sub(r"\1", out)
    out = _HEADING.sub("", out)
    out = out.replace("**", "").replace("__", "")
    out = _MULTI_NL.sub("\n\n", out)
    return out.strip()


def scrub(text: str) -> str:
    """Ensure banned product names never appear; return plain text."""
    if not text:
        return text
    if _BANNED.search(text):
        return _SAFE_REPLY
    return to_plain_text(text)
