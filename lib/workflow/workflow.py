"""Imported modules/packages"""
from lib.workflow.subject import Subject
from lib.workflow.transition import Transition
from lib.workflow.workflow_interface import WorkflowInterface


class Workflow(WorkflowInterface):
    """
    Workflow
    """

    def can(self, subject: Subject, transition_name: str) -> bool:
        assert transition_name in subject.get_transitions()
        transition: Transition = subject.get_transitions()[transition_name]
        return subject.get_state() in transition.from_states and (transition.guard is None or transition.guard(subject))

    def apply(self, subject: Subject, transition_name: str):
        assert self.can(subject, transition_name)
        transition: Transition = subject.get_transitions()[transition_name]
        subject.set_state(transition.to_state)
        if transition.completed is not None:
            transition.completed(subject)
