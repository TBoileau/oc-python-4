"""Imported modules/packages"""
from typing import Dict, Type, Union

from tinydb import TinyDB
from tinydb.table import Table

from lib.dependency_injection.container_interface import ContainerInterface
from lib.orm.entity_manager_interface import EntityManagerInterface
from lib.orm.persistent import Persistent
from lib.orm.repository import Repository


class EntityManager(EntityManagerInterface):
    """
    EntityManager class
    """
    __repositories: Dict[Type, Repository] = {}

    def __init__(self, container: ContainerInterface):
        self.__tiny_db: TinyDB = container.get(TinyDB)
        self.__container: ContainerInterface = container

    def get_table(self, table: str) -> Table:
        return self.__tiny_db.table(table)

    def get_repository(self, entity: Union[Type, Persistent]) -> Repository:
        return self.__container.get(getattr(entity, 'get_repository')())

    def persist(self, entity: Persistent):
        repository: Repository = self.get_repository(entity)
        entity.identifier = repository.table.insert(entity.serialize())
        repository.data[entity.identifier] = entity

    def update(self, entity: Persistent):
        repository: Repository = self.get_repository(entity)
        repository.table.update(entity.serialize(), doc_ids=[entity.identifier])
        repository.data[entity.identifier] = entity
