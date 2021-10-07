"""Imported modules/packages"""
from typing import Dict

from src.dependency_injection.container import ContainerInterface
from src.router.route import Route
from src.router.router_interface import RouterInterface


class Router(RouterInterface):
    """
    Router
    """

    __routes: Dict[str, Route] = {}

    def __init__(self, container: ContainerInterface):
        self.__container: ContainerInterface = container

    def add(self, route: Route) -> "RouterInterface":
        assert route.name not in self.__routes
        self.__routes[route.name] = route
        return self

    def generate(self, name: str):
        assert name in self.__routes
        self.__routes[name].call(self.__container)
