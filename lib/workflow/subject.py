"""Imported modules/packages"""
from abc import ABC
from typing import Dict

from lib.workflow.transition import Transition


class Subject(ABC):
    """
    Subject interface
    """

    def get_state(self) -> str:
        """
        Get state

        :return:
        """

    def set_state(self, state: str):
        """
        Set state

        :return:
        """

    def get_transitions(self) -> Dict[str, Transition]:
        """
        Get transitions

        :return:
        """
