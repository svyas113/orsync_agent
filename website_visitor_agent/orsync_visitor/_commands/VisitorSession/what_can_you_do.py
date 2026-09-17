import fastworkflow
from fastworkflow.train.generate_synthetic import generate_diverse_utterances

from ...application.session import VisitorSession
from ...application.sanitize import scrub


class Signature:
    plain_utterances = [
        "what can you do",
        "how can you help me",
        "show me the menu",
        "what are my options",
        "help",
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
    ) -> fastworkflow.CommandOutput:
        session: VisitorSession = workflow.command_context_for_response_generation
        response = session.what_can_you_do()
        return fastworkflow.CommandOutput(
            workflow_id=workflow.id,
            command_responses=[fastworkflow.CommandResponse(response=scrub(response))],
        )
