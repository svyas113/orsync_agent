import fastworkflow
from fastworkflow.train.generate_synthetic import generate_diverse_utterances
from pydantic import BaseModel, Field

from ...application.session import VisitorSession
from ...application.sanitize import scrub


class Signature:
    class Input(BaseModel):
        name: str = Field(
            description="Visitor's full name",
            examples=["Ada Lovelace", "Jordan Lee"],
            min_length=2,
            max_length=120,
        )
        email: str = Field(
            description="Visitor's email address for follow-up",
            examples=["ada@example.com", "jordan@company.com"],
            pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        )
        company: str = Field(
            description="Company or organization name",
            examples=["Acme Retail", "Northwind"],
            default="",
            max_length=160,
        )
        message: str = Field(
            description="What the visitor wants to see or discuss",
            examples=[
                "Custom support agent for our Shopify store",
                "Retail demo walkthrough for our team",
            ],
            default="",
            max_length=1000,
        )
        interest: str = Field(
            description="Demo interest type",
            examples=["custom agent", "retail demo", "general demo"],
            default="general demo",
            max_length=120,
        )

    plain_utterances = [
        "I want a demo",
        "request a demo",
        "book a private demo with Or-sync",
        "please have someone demo your agents for me",
        "contact me about a custom agent",
        "schedule a demo with Or-sync",
    ]

    @staticmethod
    def generate_utterances(
        workflow: fastworkflow.Workflow, command_name: str
    ) -> list[str]:
        return [
            command_name.split("/")[-1].lower().replace("_", " ")
        ] + generate_diverse_utterances(Signature.plain_utterances, command_name)


class ResponseGenerator:
    def __call__(
        self,
        workflow: fastworkflow.Workflow,
        command: str,
        command_parameters: Signature.Input,
    ) -> fastworkflow.CommandOutput:
        session: VisitorSession = workflow.command_context_for_response_generation
        result = session.request_demo(
            name=command_parameters.name,
            email=command_parameters.email,
            company=command_parameters.company,
            message=command_parameters.message,
            interest=command_parameters.interest,
        )
        return fastworkflow.CommandOutput(
            workflow_id=workflow.id,
            command_responses=[fastworkflow.CommandResponse(response=scrub(result.detail))],
        )
