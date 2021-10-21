"""Imported modules/packages"""
from abc import ABC
from typing import Type

from tinydb.table import Table

from lib.orm.persistent import Persistent


class EntityManagerInterface(ABC):
    """
    EntityManager interface
    """

    def get_table(self, table: str) -> Table:
        """
        Get table of tiny db
        :param table:
        :return:
        """

    def get_repository(self, entity: Type):
        """
        Get repository by entity
        :param entity:
        :return:
        """

    def persist(self, entity: Persistent):
        """
        Persist entity
        :param entity:
        :return:
        """

    def update(self, entity: Persistent):
        """
        Update entity
        :param entity:
        :return:
        """
