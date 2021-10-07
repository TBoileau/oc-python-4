"""Imported modules/packages"""
import importlib
import inspect
from types import ModuleType
from typing import Any, Dict, List, Type, Union

from src.dependency_injection.container_interface import ContainerInterface


class Container(ContainerInterface):
    """
    Container class
    """

    __instances: Dict[Union[Type, Any], Any] = {}
    __alias: Dict[Union[Type, Any], str] = {}
    __parameters: Dict[str, Any] = {}

    def __init__(self):
        self.__instances["container"] = self
        self.alias(ContainerInterface, Container)

    @staticmethod
    def get_type(name: Union[Type, str]) -> str:
        """
        Get type from class

        :param name:
        :return:
        """
        if isinstance(name, str):
            return name
        return f"{inspect.getmodule(name).__name__}.{name.__name__}"

    @staticmethod
    def get_instance(type_: str, args: List[Any]) -> object:
        """
        Create an instance

        :param type_:
        :param args:
        :return:
        """
        module: ModuleType = importlib.import_module(type_[0: type_.rfind(".")])
        return getattr(module, type_[type_.rfind(".") + 1:])(*args)

    def get(self, name: Union[Type, str]) -> Any:
        if name in self.__parameters:
            return self.__parameters[name]

        service_id: str = self.get_type(name)

        if service_id in self.__alias:
            return self.get(self.__alias[Container.get_type(name)])

        if service_id not in self.__instances:
            args: List[Any] = []
            if len(inspect.signature(name.__init__).parameters) > 1:
                for arg, type_ in inspect.signature(name.__init__).parameters.items():
                    if arg in ["self", "args", "kwargs"]:
                        continue
                    args.append(self.get(type_.annotation if type_.annotation.__name__ != "str" else arg))
            self.__instances[service_id] = Container.get_instance(service_id, args)

        return self.__instances[service_id]

    def alias(self, alias: Union[Type, Any], name: Union[Type, Any]):
        self.__alias[Container.get_type(alias)] = name
        return self

    def set_parameter(self, name: str, value: Any) -> "Container":
        self.__parameters[name] = value
        return self
