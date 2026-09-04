"""Qualify a sales lead by capturing use case and context."""

import fastworkflow
from fastworkflow.train.generate_synthetic import generate_diverse_utterances
from pydantic import BaseModel, Field

from ..application.orsync import company, to_customer_text


class Signature:
    class Input(BaseModel):
        use_case: str = Field(
            description="What the business wants the AI agent to do",
            examples=[
                "Sales agent on WhatsApp for lead qualification",
                "Customer support agent for order tracking",
                "Marketing content agent for Instagram",
                "Internal ops agent connected to our CRM",
            ],
            min_length=5,
            max_length=500,
        )
        industry: str = Field(
            description="Industry or business type",
            examples=["E-commerce", "Healthcare", "SaaS", "Real estate", "Education"],
            min_length=2,
            max_length=100,
        )
        current_tools: str = Field(
            description="Existing tools or platforms the agent should integrate with",
            examples=["Shopify and HubSpot", "WhatsApp Business API", "Salesforce", "Slack"],
            min_length=2,
            max_length=300,
        )
        timeline: str = Field(
            description="When they want to launch or start the project",
            examples=["ASAP", "Within 1 month", "Next quarter", "Exploring options"],
            min_length=2,
            max_length=100,
        )
        name: str | None = Field(
            default=None,
            description="Optional contact name",
            examples=["Priya Sharma", "John Smith"],
        )
        email: str | None = Field(
            default=None,
            description="Optional email for follow-up",
            examples=["priya@company.com"],
        )
        channel: str = Field(
            default="web",
            description="Channel the user came from",
            examples=["web", "whatsapp", "instagram", "ads"],
        )

    plain_utterances = [
        "I need an AI agent for my business",
        "Help me figure out if an agent is right for us",
        "We want to automate customer support on WhatsApp",
        "I'm looking for a sales agent for Instagram DMs",
        "Can you help qualify my project?",
        "We saw your ad and want an agent for lead capture",
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
            lead_type="qualified_lead",
            name=command_parameters.name,
            email=command_parameters.email,
            use_case=command_parameters.use_case,
            industry=command_parameters.industry,
            current_tools=command_parameters.current_tools,
            timeline=command_parameters.timeline,
            channel=command_parameters.channel or "web",
        )

        response = to_customer_text(
            "Great — here's what I've captured about your project:\n\n"
            f"Use case: {lead['use_case']}\n"
            f"Industry: {lead['industry']}\n"
            f"Tools: {lead['current_tools']}\n"
            f"Timeline: {lead['timeline']}\n\n"
            "Based on this, Or-sync can help you get an agent built, connected to your tools, "
            "and rolled out with a clear plan.\n\n"
            "Would you like to request a demo, or do you have pricing questions "
            "(a teammate can take over for that)?"
        )

        return fastworkflow.CommandOutput(
            command_responses=[fastworkflow.CommandResponse(response=response)]
        )
