"""Imported modules/packages"""
from abc import ABC
from typing import Dict, Any, Optional, Callable

from src.input.input import Input


class Form(ABC):
    """
    Form class
    """

    def __init__(self, handler: Callable, data: Any = None):
        self.data: Optional[Any] = data
        self.handler: Callable = handler

    def _build(self, inputs: Dict[str, Input]):
        """
        Build form

        :param inputs:
        :return:
        """

    def _transform(self, values: Dict[str, Any], data: Any = None) -> Any:
        """
        Transform data

        :param values:
        :param data:
        :return:
        """

    def handle(self):
        """
        Handle form
        """
        inputs: Dict[str, Input] = {}
        self._build(inputs)
        data: Dict[str, Any] = {}
        for name, input_ in inputs.items():
            data[name] = input_.capture()
        self.handler(self._transform(values=data, data=self.data))
