"""Imported modules/packages"""
from abc import ABC
from typing import Callable, Dict, Any

from src.form.form import Form
from src.input.input import Input
from src.router.router import RouterInterface
from src.templating.templating import TemplatingInterface


class AbstractController(ABC):
    """
    Abstract controller
    """

    def __init__(self, templating: TemplatingInterface, router: RouterInterface):
        self.__templating: TemplatingInterface = templating
        self.__router: RouterInterface = router

    def render(self, view: str, data=None):
        """
        Render view

        :param input_:
        :param choices:
        :param view:
        :param data:
        :return:
        """
        print(self.__templating.render(view, data))

    def redirect(self, name: str):
        """
        Redirect to route

        :param name:
        :return:
        """
        print(
            """
_______________________________________________________________________________
        """
        )
        self.__router.generate(name)

    def _choice(self, input_: Input, choices: Dict[int, Callable], view: str, data=None):
        """
        Render choice

        :param input_:
        :param choices:
        :param view:
        :param data:
        """
        print(self.__templating.render(view, data))
        choices[input_.capture()]()

    def _form(self, form: Form, view: str, data=None) -> Any:
        """
        Render form

        :param form:
        :param view:
        :param data:
        :return:
        """
        print(self.__templating.render(view, data))
        form.handle()
