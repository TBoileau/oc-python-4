"""Imported modules/packages"""
from lib.representation.representation import Representation
from lib.representation.representation_factory_interface import RepresentationFactoryInterface


class RepresentationFactory(RepresentationFactoryInterface):
    """
    Representation factory class
    """

    def create(self) -> Representation:
        return Representation()
