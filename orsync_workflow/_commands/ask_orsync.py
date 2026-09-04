"""Catch-all Q&A command grounded in Or-sync knowledge base."""

import dspy
import fastworkflow
from fastworkflow.train.generate_synthetic import generate_diverse_utterances
from fastworkflow.utils.dspy_utils import get_lm
from pydantic import BaseModel, Field

from ..application.orsync import company, to_customer_text


class Signature:
    class Input(BaseModel):
        question: str = Field(
            description=(
                "The user's question about Or-sync, AI agents, services, "
                "Flux Designer, integrations, or how we keep agents affordable"
            ),
            examples=[
                "What does Or-sync do?",
                "Who founded Or-sync?",
                "Can you integrate with WhatsApp?",
                "What is Flux Designer?",
                "I saw your Instagram post — tell me more",
                "Do you work with small businesses?",
            ],
            min_length=3,
            max_length=1000,
        )
        channel: str = Field(
            default="web",
            description="Channel the user came from",
            examples=["web", "whatsapp", "instagram", "ads"],
        )

    plain_utterances = [
        "What is Or-sync?",
        "Tell me about your company",
        "What do you do?",
        "How can AI agents help my business?",
        "I saw your ad on Google — what do you offer?",
        "Someone shared your Instagram — what is this?",
        "Are you different from ChatGPT bots?",
        "Can you help with sales and marketing automation?",
    ]

    @staticmethod
    def generate_utterances(workflow: fastworkflow.Workflow, command_name: str) -> list[str]:
        return [
            command_name.split("/")[-1].lower().replace("_", " "),
        ] + generate_diverse_utterances(Signature.plain_utterances, command_name)


class AnswerSignature(dspy.Signature):
    """Answer a user question about Or-sync using only the provided knowledge base."""

    knowledge_base: str = dspy.InputField(desc="Official Or-sync company knowledge")
    question: str = dspy.InputField(desc="User's question")
    answer: str = dspy.OutputField(
        desc=(
            "Helpful plain-text answer for a non-technical business owner, grounded in the knowledge base. "
            "No markdown. No technical internals. If cost comes up, say our framework lets us build cheaper "
            "reliable agents. Never quote prices or dollar amounts. For pricing questions, explain that "
            "pricing is customized and a teammate will follow up. Encourage demos when appropriate."
        )
    )


class ResponseGenerator:
    def __call__(
        self,
        workflow: fastworkflow.Workflow,
        command: str,
        command_parameters: Signature.Input,
    ) -> fastworkflow.CommandOutput:
        question_lower = command_parameters.question.lower()
        pricing_keywords = (
            "price", "pricing", "cost", "quote", "budget", "how much", "fee", "charge", "rate"
        )
        if any(keyword in question_lower for keyword in pricing_keywords):
            handoff = company.request_pricing_handoff(
                question=command_parameters.question,
                channel=command_parameters.channel or "web",
            )
            response = company.format_pricing_handoff_response(handoff)
            response += "\n\n<!-- HANDOFF:pricing -->"
            return fastworkflow.CommandOutput(
                command_responses=[fastworkflow.CommandResponse(response=to_customer_text(response))]
            )

        lm = get_lm("LLM_RESPONSE_GEN", "LITELLM_API_KEY_RESPONSE_GEN")
        with dspy.context(lm=lm):
            generator = dspy.ChainOfThought(AnswerSignature)
            result = generator(
                knowledge_base=company.knowledge_base(),
                question=command_parameters.question,
            )

        return fastworkflow.CommandOutput(
            command_responses=[fastworkflow.CommandResponse(response=to_customer_text(result.answer))]
        )
