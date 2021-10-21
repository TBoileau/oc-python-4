"""Imported modules/packages"""
from typing import Type

from tinydb.table import Document

from lib.orm.entity import Entity
from lib.serializer.serializable import Serializable


class Persistent(Serializable,Entity):
    """
    Persistent interface
    """
    identifier: int

    @staticmethod
    def get_repository() -> Type:
        """
        Get repository

        :return:
        """

    @staticmethod
    def create(data: Document, entity_manager) -> "Persistent":
        pass
