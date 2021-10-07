"""Imported modules/packages"""
from abc import ABC
from typing import Any, List

from src.representation.header import Header


class RepresentationInterface(ABC):
    """
    Representation interface
    """

    def add_header(self, header: Header):
        """
        Add header

        :param header:
        :return:
        """

    def set_data(self, data: List[Any]):
        """
        set data
        :param data:
        :return:
        """

    def render(self):
        """
        Render representation
        :return:
        """
