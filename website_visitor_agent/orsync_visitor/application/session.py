"""Root session context for the Or-sync website visitor agent."""

from __future__ import annotations

from . import brand_knowledge, demos
from .emailer import DemoLead, EmailResult, send_demo_request_email
from .sanitize import scrub


class VisitorSession:
    """Stateful root context for website visitor conversations."""

    def what_can_you_do(self) -> str:
        return scrub(brand_knowledge.format_capabilities())

    def explain_ai_agents(self) -> str:
        return scrub(
            f"{brand_knowledge.AI_AGENTS_EXPLAINER}\n\n"
            f"{brand_knowledge.WHAT_WE_DO}"
        )

    def about_orsync(self) -> str:
        return scrub(brand_knowledge.format_about())

    def list_services(self) -> str:
        return scrub(brand_knowledge.format_services())

    def open_demo_agent(self, agent_name: str = "", random_pick: bool = False) -> str:
        name = (agent_name or "").strip().lower()

        # Discontinued names — never acknowledge them in replies.
        if "flux" in name:
            return scrub(
                "I can help with Or-sync company info, our services, "
                "public demos (Spyran, Zebrata, RVD Jewels), or a private demo request. "
                "What would you like to explore?"
            )

        if random_pick or name in {"random", "any", "surprise"}:
            demo = demos.pick_random_demo()
            return scrub(
                f"Here's a random demo pick — {demo.name}.\n\n"
                f"{demos.format_demo_handoff(demo)}"
            )

        if not name:
            return scrub(demos.format_all_demos())

        demo = demos.find_demo(agent_name)
        if demo is None:
            return scrub(
                "I don't have a public demo by that name. "
                "Our public demos are Spyran, Zebrata, and RVD Jewels — "
                "or I can request a private demo for your use case."
            )
        return scrub(demos.format_demo_handoff(demo))

    def request_demo(
        self,
        name: str,
        email: str,
        company: str = "",
        message: str = "",
        interest: str = "general demo",
    ) -> EmailResult:
        clean_interest = interest or "general demo"
        if "flux" in clean_interest.lower():
            clean_interest = "custom agent demo"
        clean_message = message or ""
        if "flux" in clean_message.lower():
            clean_message = "Interested in a custom Or-sync agent demo."

        lead = DemoLead(
            name=name.strip(),
            email=email.strip(),
            company=(company or "").strip(),
            message=clean_message.strip(),
            interest=clean_interest.strip(),
        )
        result = send_demo_request_email(lead)
        return EmailResult(ok=result.ok, detail=scrub(result.detail))
