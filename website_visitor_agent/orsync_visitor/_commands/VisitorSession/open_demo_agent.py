import fastworkflow
from fastworkflow.train.generate_synthetic import generate_diverse_utterances
from pydantic import BaseModel, Field

from ...application.session import VisitorSession
from ...application.sanitize import scrub


class Signature:
    class Input(BaseModel):
        agent_name: str = Field(
            description=(
                "Demo agent to open: Spyran, Zebrata, RVD Jewels, "
                "or random. Leave empty to list demos."
            ),
            examples=["Spyran", "Zebrata", "RVD Jewels", "random"],
            default="",
        )
        random_pick: bool = Field(
            description="True when the visitor wants any random public demo agent",
            examples=[True, False],
            default=False,
        )

    plain_utterances = [
        "I want to test your agents",
        "chat with a random demo agent",
        "show me a random demo",
        "open the Spyran demo",
        "let me try Zebrata",
        "open RVD Jewels agent",
        "I want to try one of your agents",
        "give me a demo agent to chat with",
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
        response = session.open_demo_agent(
            agent_name=command_parameters.agent_name,
            random_pick=command_parameters.random_pick,
        )
        return fastworkflow.CommandOutput(
            workflow_id=workflow.id,
            command_responses=[fastworkflow.CommandResponse(response=scrub(response))],
        )
