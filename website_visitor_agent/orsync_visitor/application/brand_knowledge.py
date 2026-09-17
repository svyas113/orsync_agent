"""Curated Or-sync brand copy sourced from the public company website."""

COMPANY_NAME = "Or-sync"
FOUNDED_YEAR = "2026"
CONTACT_EMAIL = "orsyncagents@gmail.com"
WEBSITE = "https://www.orsync.co.in"

ABOUT_SUMMARY = (
    "Or-sync was founded in 2026 on a simple belief: every business deserves "
    "production-grade AI agents — state-of-the-art technology at the most affordable price. "
    "We were founded by engineers who were part of the core team that developed fastWorkflow, "
    "an open-source framework for building large-scale, deterministic, interactive agent workflows. "
    "On industry-standard Tau Bench benchmarks, fastWorkflow enables small models to match "
    "frontier model performance on structured agentic tasks."
)

MISSION = (
    "State-of-the-art agent technology at the lowest possible cost. "
    "We make production-grade AI accessible to businesses of every size."
)

VALUES = [
    {
        "title": "Purpose-Built",
        "description": (
            "Every agent we create is designed for a specific use case — "
            "no generic solutions, no one-size-fits-all."
        ),
    },
    {
        "title": "Transparent",
        "description": (
            "We believe in clear communication about what AI can and cannot do. "
            "No hype, just results."
        ),
    },
    {
        "title": "Affordable by Design",
        "description": (
            "State-of-the-art agent technology at the lowest possible cost — "
            "small models that perform like frontier ones."
        ),
    },
    {
        "title": "User-First",
        "description": (
            "We design agents that feel natural to interact with, "
            "prioritizing the end-user experience above all."
        ),
    },
]

SERVICES = [
    {
        "title": "Custom Agent Development",
        "description": (
            "We design and build AI agents from scratch based on your specific business "
            "requirements — from e-commerce to internal ops."
        ),
    },
    {
        "title": "Platform Integration",
        "description": (
            "Connect your AI agent to the tools you already use: Shopify, CRMs, "
            "Slack/Teams, and custom APIs."
        ),
    },
    {
        "title": "Agent Strategy & Consulting",
        "description": (
            "Identify high-impact use cases and get a practical implementation roadmap."
        ),
    },
    {
        "title": "Optimization & Scaling",
        "description": (
            "Improve accuracy, performance, and capacity for agents already in production."
        ),
    },
    {
        "title": "Maintenance & Support",
        "description": (
            "Ongoing monitoring, updates, and continuous improvement for deployed agents."
        ),
    },
    {
        "title": "Training & Workshops",
        "description": (
            "Hands-on training for your team on agent best practices and day-to-day management."
        ),
    },
]

AI_AGENTS_EXPLAINER = (
    "An AI agent is software that can understand what you want in plain language, "
    "decide which tools or steps to use, and take action — not just chat. "
    "Unlike a basic chatbot that only replies with text, Or-sync agents are built on "
    "fastWorkflow so they validate parameters, run structured workflows, and ask for "
    "clarification instead of silently doing the wrong thing."
)

WHAT_WE_DO = (
    "Or-sync delivers custom AI agents for businesses. We help you design, build, "
    "integrate, and maintain agents that plug into your existing tools. "
    "You can try our public retail demo agents (Spyran, Zebrata, RVD Jewels), "
    "or request a private demo tailored to your use case."
)


def format_about() -> str:
    value_lines = "\n".join(
        f"- {v['title']}: {v['description']}" for v in VALUES
    )
    return (
        f"{ABOUT_SUMMARY}\n\n"
        f"Mission: {MISSION}\n\n"
        f"Our values:\n{value_lines}\n\n"
        f"Website: {WEBSITE}\n"
        f"Contact: {CONTACT_EMAIL}"
    )


def format_services() -> str:
    lines = "\n".join(
        f"- {s['title']}: {s['description']}" for s in SERVICES
    )
    return (
        "Here is what Or-sync offers:\n\n"
        f"{lines}\n\n"
        "Want something custom? Ask me to request a demo and I'll notify the team."
    )


def format_capabilities() -> str:
    return (
        "I can help you with:\n"
        "1. Explain what AI agents are and what Or-sync does\n"
        "2. Tell you about the Or-sync company and brand\n"
        "3. List our services\n"
        "4. Open a public demo agent (Spyran, Zebrata, or RVD Jewels) — or pick one at random\n"
        "5. Request a private demo — that notifies orsyncagents@gmail.com\n\n"
        "What would you like to do?"
    )
