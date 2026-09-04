"""Escalate pricing questions to human takeover — never quote prices."""

import fastworkflow
from fastworkflow.train.generate_synthetic import generate_diverse_utterances
from pydantic import BaseModel, Field

from ..application.orsync import company, to_customer_text


class Signature:
    class Input(BaseModel):
        question: str = Field(
            description="The user's pricing or cost-related question",
            examples=[
                "How much does a custom agent cost?",
                "What are your pricing packages?",
                "Can you share a quote?",
                "What's the monthly cost?",
            ],
            min_length=3,
            max_length=500,
        )
        name: str | None = Field(
            default=None,
            description="Optional name for follow-up",
            examples=["Priya Sharma", "John Smith"],
        )
        email: str | None = Field(
            default=None,
            description="Optional email for follow-up",
            examples=["priya@company.com"],
        )
        use_case: str | None = Field(
            default=None,
            description="Brief description of what they need priced",
            examples=["WhatsApp sales agent", "Instagram marketing agent"],
        )
        channel: str = Field(
            default="web",
            description="Channel the user came from",
            examples=["web", "whatsapp", "instagram", "ads"],
        )

    plain_utterances = [
        "How much does it cost?",
        "What are your prices?",
        "Can you give me a quote?",
        "What's your pricing?",
        "How much for a custom AI agent?",
        "Is there a monthly fee?",
        "What's the budget for an agent project?",
        "I saw your ad — how much do you charge?",
    ]

    @staticmethod
    def generate_utterances(workflow: fastworkflow.Workflow, command_name: str) -> list[str]:
        return [
            command_name.split("/")[-1].lower().replace("_", " "),
        ] + generate_diverse_utterances(Signature.plain_utterances, command_name)


class ResponseGenerator:
    def __call__(
        self,
        workflow: fastworkflow.Workflow,
        command: str,
        command_parameters: Signature.Input,
    ) -> fastworkflow.CommandOutput:
        handoff = company.request_pricing_handoff(
            name=command_parameters.name,
            email=command_parameters.email,
            use_case=command_parameters.use_case,
            channel=command_parameters.channel or "web",
            question=command_parameters.question,
        )

        response = to_customer_text(
            company.format_pricing_handoff_response(handoff) + "\n\n<!-- HANDOFF:pricing -->"
        )

        return fastworkflow.CommandOutput(
            command_responses=[fastworkflow.CommandResponse(response=response)]
        )
