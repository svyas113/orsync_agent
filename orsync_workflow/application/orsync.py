"""Or-sync company knowledge, lead capture, and pricing handoffs."""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
LEADS_FILE = DATA_DIR / "leads.jsonl"
HANDOFFS_FILE = DATA_DIR / "handoffs.jsonl"

# TODO(next-dev): Customer replies must stay plain text (WhatsApp/Instagram). See README
# "MUST CHANGE" for remaining markdown cleanup across commands and LLM answers.


def to_customer_text(text: str) -> str:
    """Strip markdown/HTML so replies work on WhatsApp, Instagram, and ads chat."""
    keep_handoff = "<!-- HANDOFF:pricing -->" in text
    cleaned = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    cleaned = re.sub(r"\*\*(.+?)\*\*", r"\1", cleaned)
    cleaned = re.sub(r"__(.+?)__", r"\1", cleaned)
    cleaned = re.sub(r"`([^`]+)`", r"\1", cleaned)
    cleaned = re.sub(r"^#{1,6}\s+", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^[-*]\s+", "- ", cleaned, flags=re.MULTILINE)
    cleaned = cleaned.strip()
    if keep_handoff:
        cleaned = f"{cleaned}\n\n<!-- HANDOFF:pricing -->"
    return cleaned


@dataclass
class Service:
    name: str
    slug: str
    description: str
    highlights: list[str] = field(default_factory=list)


@dataclass
class Orsync:
    """Singleton knowledge store for Or-sync AI agent company."""

    name: str = "Or-sync"
    tagline: str = "Intelligent Agents Built For Your Business"
    website: str = "https://orsync.co.in/"
    founded: str = "2026"
    location: str = "Remote-first, Global"
    response_time: str = "Within 24 hours"

    pitch: str = (
        "Or-sync builds AI agents that handle sales, support, and day-to-day customer conversations "
        "for your business — at a price that smaller teams can actually afford. Our own framework "
        "lets us run capable agents without the usual enterprise AI bill."
    )

    story: str = (
        "Or-sync was founded in 2026 to make serious AI agents affordable. We built our own "
        "framework so agents can do real work — answer customers, take leads, book demos — "
        "without charging frontier-model prices. That is the advantage we pass on to you: "
        "reliable agents that cost less because of how we build them, not because we cut corners."
    )

    mission: str = (
        "State-of-the-art agent technology at the lowest possible cost. "
        "We make production-grade AI accessible to businesses of every size."
    )

    values: list[str] = field(default_factory=lambda: [
        "Purpose-Built — every agent is designed for a specific use case, not one-size-fits-all.",
        "Transparent — clear communication about what AI can and cannot do. No hype, just results.",
        "Affordable by Design — our framework keeps agent costs down without lowering quality.",
        "User-First — agents that feel natural to interact with.",
    ])

    differentiators: list[str] = field(default_factory=lambda: [
        "Agents that do real work — they can answer customers, capture leads, and book demos, not just chat.",
        "Lower cost because of our framework — we do not need the most expensive AI models to get reliable results, so you pay less.",
        "Fits the tools you already use — WhatsApp, Instagram, CRMs, shops, and your existing apps.",
        "Built to be dependable — if something is unclear, the agent asks instead of guessing.",
    ])

    services: list[Service] = field(default_factory=lambda: [
        Service(
            name="Custom Agent Development",
            slug="custom-agent-development",
            description=(
                "We design and build AI agents from scratch based on your specific business requirements. "
                "From e-commerce to internal ops, we craft agents that understand your domain."
            ),
            highlights=[
                "Domain-specific training",
                "Multi-step workflow handling",
                "Natural language understanding",
                "Custom personality and tone",
            ],
        ),
        Service(
            name="Platform Integration",
            slug="platform-integration",
            description=(
                "Connect your AI agent seamlessly to the tools and platforms you already use. "
                "We handle the technical integration so your agent works within your existing ecosystem."
            ),
            highlights=[
                "Shopify and e-commerce platforms",
                "CRM systems (Salesforce, HubSpot)",
                "Communication tools (Slack, Teams)",
                "Custom API integrations",
            ],
        ),
        Service(
            name="Agent Strategy & Consulting",
            slug="agent-strategy-consulting",
            description=(
                "Not sure where to start? We help you identify the highest-impact areas for AI agent "
                "deployment and design a roadmap for implementation."
            ),
            highlights=[
                "Use case identification",
                "ROI analysis",
                "Architecture planning",
                "Implementation roadmap",
            ],
        ),
        Service(
            name="Optimization & Scaling",
            slug="optimization-scaling",
            description=(
                "Already have agents in production? We help optimize their performance, improve accuracy, "
                "and scale to handle growing demand."
            ),
            highlights=[
                "Performance analytics",
                "Response quality tuning",
                "Load scaling",
                "A/B testing frameworks",
            ],
        ),
        Service(
            name="Maintenance & Support",
            slug="maintenance-support",
            description=(
                "Keep your agents running smoothly with ongoing maintenance packages. "
                "We monitor, update, and improve your agents continuously."
            ),
            highlights=[
                "24/7 monitoring",
                "Regular model updates",
                "Bug fixes and patches",
                "Monthly performance reports",
            ],
        ),
        Service(
            name="Training & Workshops",
            slug="training-workshops",
            description=(
                "Empower your team with hands-on training on AI agent best practices, "
                "prompt engineering, and managing deployed agents."
            ),
            highlights=[
                "Team workshops",
                "Prompt engineering training",
                "Agent management guides",
                "Best practices documentation",
            ],
        ),
    ])

    process_steps: list[dict[str, str]] = field(default_factory=lambda: [
        {"step": "Discovery", "description": "We learn about your business, workflows, and goals to identify the perfect use case for an AI agent."},
        {"step": "Design", "description": "We architect the agent's capabilities, integrations, and conversation flows tailored to your needs."},
        {"step": "Build", "description": "Our engineering team develops your agent with rigorous testing at every stage."},
        {"step": "Deploy & Iterate", "description": "We launch your agent and continuously improve it based on real-world performance data."},
    ])

    flux_designer: str = (
        "Flux Designer is Or-sync's own marketing agent. Every post on our Instagram and LinkedIn "
        "is generated by Flux Designer — that's our live portfolio. Because it's connected to our "
        "accounts, we can't offer public access. Contact us for a private demo."
    )

    contact_topics: list[str] = field(default_factory=lambda: [
        "Custom Agent Development",
        "Request a Demo",
        "Strategy & Consulting",
        "Partnership",
    ])

    faqs: list[dict[str, str]] = field(default_factory=lambda: [
        {
            "question": "What does Or-sync do?",
            "answer": (
                "Or-sync builds AI agents for businesses — custom agents, connections to your existing "
                "tools, strategy help, ongoing improvement, support, and team training. "
                "Our own framework is what lets us offer this at a lower cost."
            ),
        },
        {
            "question": "Why are Or-sync agents more affordable?",
            "answer": (
                "Because we built our own agent framework. It lets us create reliable agents without "
                "depending on the most expensive AI setups, so we can charge less than typical "
                "enterprise AI shops. We do not walk customers through the technical internals — "
                "the takeaway is simple: same quality of agent, lower cost."
            ),
        },
        {
            "question": "Do you publish pricing?",
            "answer": (
                "No — pricing depends on your use case, integrations, and scope. We never quote fixed "
                "packages in chat. A teammate will follow up to discuss pricing after understanding your needs."
            ),
        },
        {
            "question": "Can I see Flux Designer?",
            "answer": (
                "Flux Designer powers our own Instagram and LinkedIn content. Because it's connected to "
                "our accounts, we offer private demos on request — not public access."
            ),
        },
        {
            "question": "How quickly do you respond?",
            "answer": "We respond within 24 hours. Email us at orsyncagents@gmail.com or use this chat to request a demo.",
        },
    ])

    contact: dict[str, str] = field(default_factory=lambda: {
        "email": "orsyncagents@gmail.com",
        "website": "https://orsync.co.in/",
        "location": "Remote-first, Global",
        "response_time": "Within 24 hours",
    })

    pricing_policy: str = (
        "NEVER quote specific prices, packages, retainers, or dollar amounts. "
        "Or-sync does not publish public pricing. When users ask about cost, pricing, quotes, "
        "budget, or 'how much', explain that pricing is customized and a teammate will take over "
        "the conversation to discuss their specific needs."
    )

    _leads: list[dict[str, Any]] = field(default_factory=list)
    _handoffs: list[dict[str, Any]] = field(default_factory=list)

    def _ensure_data_dir(self) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    def _append_jsonl(self, path: Path, record: dict[str, Any]) -> None:
        self._ensure_data_dir()
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    def list_service_names(self) -> list[str]:
        return [service.name for service in self.services]

    def get_service_by_name(self, name: str) -> Service | None:
        normalized = name.lower().strip()
        for service in self.services:
            if service.name.lower() == normalized or service.slug.lower() == normalized:
                return service
            if normalized in service.name.lower():
                return service
            if normalized in service.slug.replace("-", " "):
                return service
        return None

    def format_services_list(self) -> str:
        lines = ["Or-sync services\n"]
        for index, service in enumerate(self.services, 1):
            lines.append(f"{index}. {service.name} — {service.description}")
        lines.append(
            "\nWould you like details on a specific service, or shall I help you book a demo?"
        )
        return to_customer_text("\n".join(lines))

    def format_service_details(self, service: Service) -> str:
        highlights = ", ".join(service.highlights)
        return to_customer_text(
            f"{service.name}\n\n"
            f"{service.description}\n\n"
            f"Key highlights: {highlights}\n\n"
            "Interested? I can help you request a demo or connect you with our team."
        )

    def format_contact_info(self) -> str:
        contact = self.contact
        return to_customer_text(
            f"Contact Or-sync\n\n"
            f"Email: {contact['email']}\n"
            f"Website: {contact['website']}\n"
            f"Location: {contact['location']}\n"
            f"Response time: {contact['response_time']}\n\n"
            "Topics we can help with: Custom Agent Development, Request a Demo, "
            "Strategy & Consulting, or Partnership."
        )

    def format_approach(self) -> str:
        differentiators = "\n".join(f"- {item}" for item in self.differentiators)
        process = "\n".join(
            f"- {step['step']}: {step['description']}" for step in self.process_steps
        )
        return to_customer_text(
            "Why businesses choose Or-sync\n\n"
            f"{self.pitch}\n\n"
            "Why our agents cost less\n"
            f"{self.story}\n\n"
            f"What that means for you\n{differentiators}\n\n"
            f"How we work\n{process}\n\n"
            f"A live example — Flux Designer\n{self.flux_designer}"
        )

    def capture_lead(
        self,
        *,
        lead_type: str,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        use_case: str | None = None,
        industry: str | None = None,
        current_tools: str | None = None,
        timeline: str | None = None,
        channel: str | None = None,
        message: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        record = {
            "type": lead_type,
            "name": name or "",
            "email": email or "",
            "phone": phone or "",
            "use_case": use_case or "",
            "industry": industry or "",
            "current_tools": current_tools or "",
            "timeline": timeline or "",
            "channel": channel or "web",
            "message": message or "",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        if extra:
            record.update(extra)
        self._leads.append(record)
        self._append_jsonl(LEADS_FILE, record)
        logger.info("Lead captured (%s): %s", lead_type, json.dumps(record))
        return record

    def request_pricing_handoff(
        self,
        *,
        name: str | None = None,
        email: str | None = None,
        use_case: str | None = None,
        channel: str | None = None,
        question: str | None = None,
    ) -> dict[str, Any]:
        record = {
            "type": "pricing_handoff",
            "name": name or "",
            "email": email or "",
            "use_case": use_case or "",
            "channel": channel or "web",
            "question": question or "",
            "status": "pending_human_takeover",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._handoffs.append(record)
        self._append_jsonl(HANDOFFS_FILE, record)
        logger.info("Pricing handoff requested: %s", json.dumps(record))
        return record

    def format_pricing_handoff_response(self, record: dict[str, Any]) -> str:
        greeting = f"Thanks, {record['name']}! " if record.get("name") else "Thanks! "
        return to_customer_text(
            f"{greeting}Pricing at Or-sync is customized to your use case — we don't publish "
            "fixed packages or quote amounts in chat.\n\n"
            "A teammate will take over this conversation shortly to understand your needs "
            "and share pricing options.\n\n"
            f"In the meantime, you can email us at {self.contact['email']} "
            f"or explore our services at {self.contact['website']}."
        )

    def knowledge_base(self) -> str:
        services_text = "\n".join(f"- {service.name}: {service.description}" for service in self.services)
        faq_text = "\n".join(
            f"Q: {item['question']}\nA: {item['answer']}" for item in self.faqs
        )
        values_text = "\n".join(f"- {value}" for value in self.values)
        contact = self.contact

        return f"""
Or-sync — company knowledge for customer chat

Overview
- Company: {self.name}
- Tagline: {self.tagline}
- Founded: {self.founded}
- Location: {self.location}
- Website: {contact['website']}
- Email: {contact['email']}
- Response time: {contact['response_time']}

Pitch
{self.pitch}

Our story (keep this simple for customers)
{self.story}

Mission
{self.mission}

Values
{values_text}

Services
{services_text}

Flux Designer (marketing agent example)
{self.flux_designer}

Contact topics
{', '.join(self.contact_topics)}

Frequently asked questions
{faq_text}

Pricing policy (CRITICAL)
{self.pricing_policy}

Response guidelines
- Write for non-technical business owners. Short, clear, no jargon.
- NEVER explain framework internals, models, benchmarks, Tau Bench, BERT, intent classifiers, or similar.
- If asked why we are affordable: say our own framework lets us build reliable agents at a lower cost.
- Do not name fastWorkflow, FastWorkflow, or similar technical product names in customer replies unless the user specifically asks for the framework name.
- Use plain text only. No markdown, no **bold**, no headings, no code fences, no emoji-heavy formatting.
- Or-sync builds AI agents that do real work — not generic chatbots.
- For pricing questions: never invent numbers. Explain customization and offer human handoff.
- Encourage demo requests.
- Do not invent clients, case studies, or guarantees not listed above.
- You may share the website: {contact['website']}
""".strip()


company = Orsync()
