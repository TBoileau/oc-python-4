"""Imported modules/packages"""
from src.representation.representation import Representation
from src.representation.representation_factory_interface import RepresentationFactoryInterface


class RepresentationFactory(RepresentationFactoryInterface):
    """
    Representation factory class
    """

    def create(self) -> Representation:
        return Representation()
