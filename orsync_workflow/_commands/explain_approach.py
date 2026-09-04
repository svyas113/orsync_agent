"""Explain Or-sync's approach in plain language for non-technical customers."""

import fastworkflow
from fastworkflow.train.generate_synthetic import generate_diverse_utterances
from pydantic import BaseModel

from ..application.orsync import company


class Signature:
    class Input(BaseModel):
        pass

    plain_utterances = [
        "Why should I choose Or-sync?",
        "What makes you different from other AI companies?",
        "Why are your agents cheaper?",
        "How is this different from a chatbot?",
        "Why should I trust your agents?",
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
        response = company.format_approach()
        return fastworkflow.CommandOutput(
            command_responses=[fastworkflow.CommandResponse(response=response)]
        )
