"""Imported modules/packages"""
from typing import Type, List, Any

from src.dependency_injection.container import ContainerInterface


class Route:
    """
    Route class
    """

    def __init__(self, name: str, controller: Type, action: str):
        """
        Constructor

        :param name:
        :param controller:
        :param action:
        """
        self.name: str = name
        self.controller: Type = controller
        self.action: str = action

    def call(self, container: ContainerInterface, params: List[Any] = None):
        """
        Call the callback

        :param container:
        :param params:
        :return:
        """
        if params is None:
            params = []
        getattr(container.get(self.controller), self.action)(*params)
