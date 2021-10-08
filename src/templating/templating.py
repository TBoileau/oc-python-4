"""Imported modules/packages"""
import locale
import os.path

from src.templating.templating_interface import TemplatingInterface


class Templating(TemplatingInterface):
    """
    Templating
    """

    def __init__(self, templating_directory: str):
        self.__directory: str = templating_directory

    def render(self, view: str, data=None) -> str:
        if data is None:
            data = {}
        with open(os.path.join(self.__directory, view), encoding=locale.getpreferredencoding()) as template:
            return str(template.read()).format(**data)
