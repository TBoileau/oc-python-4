"""Imported modules/packages"""
from typing import Callable


class Header:
    """
    Header
    """

    def __init__(self, order: int, label: str, callback: Callable):
        """
        Constructor

        :param order:
        :param label:
        :param callback:
        """
        self.order: int = order
        self.label: str = label
        self.callback: Callable = callback
        self.length: int = len(label)
