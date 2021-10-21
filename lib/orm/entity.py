"""Imported modules/packages"""
from abc import ABC

from tinydb.table import Document


class Entity(ABC):
    """
    Entity interface
    """

    @staticmethod
    def create(data: Document, entity_manager) -> "Entity":
        """
        Create an instance
        :param data:
        :param entity_manager:
        :return:
        """
