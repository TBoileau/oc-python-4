"""Imported modules/packages"""
import locale
import os.path
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


class Templating(TemplatingInterface):
    """
    Templating
    """

    def __init__(self, directory: str):
        self.__directory: str = directory

    def render(self, view: str, data=None) -> str:
        if data is None:
            data = {}
        with open(os.path.join(self.__directory, view), encoding=locale.getpreferredencoding()) as template:
            return str(template.read()).format(data)
