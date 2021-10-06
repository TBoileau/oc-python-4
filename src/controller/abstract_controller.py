"""Imported modules/packages"""
from abc import ABC
from typing import Dict, Callable

from src.templating.templating import TemplatingInterface


class AbstractController(ABC):
    """
    Abstract controller
    """

    def __init__(self, templating: TemplatingInterface):
        self.__templating: TemplatingInterface = templating

    def _render(self, view: str, data=None):
        """
        Render view

        :param view:
        :param data:
        :return:
        """
        print(self.__templating.render(view, data))

    @staticmethod
    def redirect(label: str, choices: Dict[int, Callable]):
        """
        Redirect

        :param label:
        :param choices:
        :return:
        """
        choice: int = int(input(label))
        choices[choice]()
