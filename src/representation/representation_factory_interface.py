"""Imported modules/packages"""
from abc import ABC

from src.representation.representation import Representation


class RepresentationFactoryInterface(ABC):
    """
    Representation factory interface
    """

    def create(self) -> Representation:
        """
        Create a representation

        :return:
        """
