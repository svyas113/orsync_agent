import fastworkflow

from ..application.session import VisitorSession
from ..application.sanitize import scrub


class ResponseGenerator:
    def __call__(
        self,
        workflow: fastworkflow.Workflow,
        command: str,
    ) -> fastworkflow.CommandOutput:
        if workflow.root_command_context is None:
            workflow.root_command_context = VisitorSession()

        response = (
            "Hi — I'm the Or-sync site assistant. "
            "I can explain AI agents, tell you about Or-sync, open a public demo agent, "
            "or request a private demo for you."
        )

        return fastworkflow.CommandOutput(
            workflow_id=workflow.id,
            command_responses=[
                fastworkflow.CommandResponse(response=scrub(response))
            ],
        )
