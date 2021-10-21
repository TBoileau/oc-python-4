"""Imported modules/packages"""
from typing import Callable

from lib.representation.representation import Representation
from lib.representation.representation_factory_interface import RepresentationFactoryInterface


class RepresentationFactory(RepresentationFactoryInterface):
    """
    Representation factory class
    """

    def create(self, callback: Callable) -> Representation:
        return Representation(callback)
