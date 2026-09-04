"""List all Or-sync services."""

import fastworkflow
from fastworkflow.train.generate_synthetic import generate_diverse_utterances
from pydantic import BaseModel

from ..application.orsync import company


class Signature:
    class Input(BaseModel):
        pass

    plain_utterances = [
        "What services do you offer?",
        "List your services",
        "What can Or-sync do for my business?",
        "Tell me about your AI agent services",
        "What do you build?",
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
        response = company.format_services_list()
        return fastworkflow.CommandOutput(
            command_responses=[fastworkflow.CommandResponse(response=response)]
        )
