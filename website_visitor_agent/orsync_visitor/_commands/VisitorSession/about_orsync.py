import fastworkflow
from fastworkflow.train.generate_synthetic import generate_diverse_utterances

from ...application.session import VisitorSession
from ...application.sanitize import scrub


class Signature:
    plain_utterances = [
        "tell me about your company",
        "I want to know more about your brand",
        "who are you",
        "about Or-sync",
        "what is Or-sync",
        "tell me about Or sync",
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
        response = session.about_orsync()
        return fastworkflow.CommandOutput(
            workflow_id=workflow.id,
            command_responses=[fastworkflow.CommandResponse(response=scrub(response))],
        )
