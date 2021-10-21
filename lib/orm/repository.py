"""Imported modules/packages"""
import importlib
import inspect
from abc import ABC
from types import ModuleType
from typing import Type, List, Dict, Optional

from lib.orm.entity_manager_interface import EntityManagerInterface
from tinydb.table import Document, Table

from lib.orm.persistent import Persistent


class Repository(ABC):
    """
    Repository interface
    """

    def __init__(self, entity_manager: EntityManagerInterface, entity: Type, table: str):
        self.__entity_manager: EntityManagerInterface = entity_manager
        self.__entity: Type = entity
        self.table: Table = self.__entity_manager.get_table(table)
        self.data: Dict[int, Persistent] = {}

    def __create_entity(self, data: Document) -> Persistent:
        type_: str = f"{inspect.getmodule(self.__entity).__name__}.{self.__entity.__name__}"
        module: ModuleType = importlib.import_module(type_[0: type_.rfind(".")])
        class_: Persistent = getattr(module, type_[type_.rfind(".") + 1:])
        return class_.create(data, self.__entity_manager)

    def find_all(self) -> List[Persistent]:
        entities: List[Persistent] = list(map(self.__create_entity, self.table.all()))

        for entity in entities:
            self.data[entity.identifier] = entity

        return list(self.data.values())

    def find(self, identifier: int) -> Optional[Persistent]:
        if identifier in self.data:
            return self.data[identifier]

        data: Optional[Document] = self.table.get(doc_id=identifier)

        if data is None:
            return None

        self.data[identifier] = self.__create_entity(data)

        return self.data[identifier]
