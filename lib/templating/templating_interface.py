"""Imported modules/packages"""
from abc import ABC


class TemplatingInterface(ABC):
    """
    Templating interface
    """

    def render(self, view: str, data=None) -> str:
        """
        Render template

        :param view:
        :param data:
        :return:
        """
