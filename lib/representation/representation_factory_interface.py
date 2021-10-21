"""Imported modules/packages"""
from abc import ABC
from typing import Callable

from lib.representation.representation import Representation


class RepresentationFactoryInterface(ABC):
    """
    Representation factory interface
    """

    def create(self, callback: Callable) -> Representation:
        """
        Create a representation

        :param callback:
        :return:
        """
