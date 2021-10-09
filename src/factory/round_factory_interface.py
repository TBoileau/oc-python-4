"""Imported modules/packages"""
from abc import ABC
from typing import Dict

from src.entity.round import Round


class RoundFactoryInterface(ABC):
    """
    Round factory interface
    """

    def create(self, data: Dict) -> Round:
        """
        Create an instance of Round

        :param data:
        :return:
        """
