"""Get detailed information about a specific Or-sync service."""

import fastworkflow
from fastworkflow.train.generate_synthetic import generate_diverse_utterances
from fastworkflow.utils.signatures import DatabaseValidator
from pydantic import BaseModel, Field

from ..application.orsync import company


class Signature:
    class Input(BaseModel):
        service_name: str = Field(
            description="Name of the Or-sync service to learn about",
            examples=[
                "Custom Agent Development",
                "Platform Integration",
                "Agent Strategy & Consulting",
                "Optimization & Scaling",
                "Maintenance & Support",
                "Training & Workshops",
            ],
            json_schema_extra={"db_lookup": True},
        )

    plain_utterances = [
        "Tell me about custom agent development",
        "What does platform integration include?",
        "Explain your consulting services",
        "How do you help optimize existing agents?",
        "What's included in maintenance and support?",
        "Do you offer training workshops?",
    ]

    @staticmethod
    def db_lookup(
        workflow: fastworkflow.Workflow,
        field_name: str,
        field_value: str,
    ) -> tuple[bool, str | None, list[str]]:
        if field_name == "service_name":
            key_values = company.list_service_names()
            matched, corrected_value, suggestions = DatabaseValidator.fuzzy_match(
                field_value, key_values
            )
            return matched, corrected_value, suggestions
        return False, "", []

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
        service = company.get_service_by_name(command_parameters.service_name)

        if not service:
            available = ", ".join(company.list_service_names())
            response = (
                f"I couldn't find a service matching '{command_parameters.service_name}'. "
                f"Our available services are: {available}. Which one would you like to know more about?"
            )
        else:
            response = company.format_service_details(service)

        return fastworkflow.CommandOutput(
            command_responses=[fastworkflow.CommandResponse(response=response)]
        )
