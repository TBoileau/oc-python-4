"""Imported modules/packages"""
from typing import Type

from lib.orm.entity import Entity
from lib.serializer.serializable import Serializable


class Persistent(Serializable,Entity):
    """
    Persistent interface
    """

    @staticmethod
    def get_repository() -> Type:
        """
        Get repository

        :return:
        """

    @property
    def identifier(self) -> int:
        """
        Get identifier
        :return:
        """

    @identifier.setter
    def identifier(self, identifier: int) -> int:
        """
        Set identifier
        :param identifier:
        :return:
        """
