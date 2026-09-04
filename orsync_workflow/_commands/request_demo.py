"""Request a demo with Or-sync."""

import fastworkflow
from fastworkflow.train.generate_synthetic import generate_diverse_utterances
from pydantic import BaseModel, Field

from ..application.orsync import company, to_customer_text


class Signature:
    class Input(BaseModel):
        name: str = Field(
            description="Full name of the person requesting a demo",
            examples=["Priya Sharma", "John Smith", "Alex Chen"],
            min_length=2,
            max_length=100,
        )
        email: str = Field(
            description="Email address for follow-up",
            examples=["priya@company.com", "john@startup.io"],
            pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        )
        phone: str | None = Field(
            default=None,
            description="Optional phone number for contact",
            examples=["+91 9876543210", "+1 5551234567"],
        )
        demo_interest: str = Field(
            description="What the user wants to see or discuss in the demo",
            examples=[
                "Custom sales agent for WhatsApp",
                "Flux Designer marketing agent demo",
                "Agent integration with our CRM",
                "Strategy session for our ecommerce business",
            ],
            min_length=5,
            max_length=500,
        )
        channel: str = Field(
            default="web",
            description="Channel the user came from (web, whatsapp, instagram, ads)",
            examples=["web", "whatsapp", "instagram", "ads"],
        )

    plain_utterances = [
        "I'd like to request a demo",
        "Can I see a demo of your agents?",
        "Book a demo with Or-sync",
        "I want to see Flux Designer in action",
        "Schedule a call to discuss an AI agent for my business",
        "Request a private demo",
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
        lead = company.capture_lead(
            lead_type="demo_request",
            name=command_parameters.name,
            email=command_parameters.email,
            phone=command_parameters.phone,
            use_case=command_parameters.demo_interest,
            channel=command_parameters.channel or "web",
            message=command_parameters.demo_interest,
        )

        phone_line = f"\nPhone: {lead['phone']}" if lead.get("phone") else ""
        response = to_customer_text(
            f"Thank you, {lead['name']}! Your demo request has been received.\n\n"
            f"Email: {lead['email']}{phone_line}\n"
            f"Interest: {lead['use_case']}\n\n"
            f"Our team will reach out within 24 hours at {company.contact['email']}. "
            "We look forward to showing you what an Or-sync agent can do for your business."
        )

        return fastworkflow.CommandOutput(
            command_responses=[fastworkflow.CommandResponse(response=response)]
        )
