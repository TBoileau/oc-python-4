"""Imported modules/packages"""
from abc import ABC

from src.workflow.subject import Subject


class WorkflowInterface(ABC):
    """
    Workflow interface
    """

    def can(self, subject: Subject, transition_name: str) -> bool:
        """
        Can apply transition

        :param subject:
        :param transition_name:
        :return:
        """

    def apply(self, subject: Subject, transition_name: str):
        """
        Apply transition

        :param subject:
        :param transition_name:
        :return:
        """
