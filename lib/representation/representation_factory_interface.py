"""Imported modules/packages"""
from abc import ABC

from lib.representation.representation import Representation


class RepresentationFactoryInterface(ABC):
    """
    Representation factory interface
    """

    def create(self) -> Representation:
        """
        Create a representation

        :return:
        """
