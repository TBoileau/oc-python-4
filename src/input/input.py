"""Imported modules/packages"""
from typing import Any, Callable

from src.helper.console import Console


class Input:
    """
    Input class
    """

    __label: str
    __message: str
    __validate: Callable
    __transform: Callable

    def __init__(
        self,
        label: str,
        message: str = "",
        transform: Callable = lambda raw_data: raw_data,
        validate: Callable = lambda raw_data: True,
    ):
        self.__label = label
        self.__message = message
        self.__transform = transform
        self.__validate = validate

    def capture(self) -> Any:
        """
        Capture the input

        :return:
        """
        while True:
            raw_data: str = Console.input(self.__label, Console.BOLD)
            if self.__validate(raw_data):
                return self.__transform(raw_data)
            Console.print(self.__message, Console.WARNING)
