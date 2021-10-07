"""Imported modules/packages"""
from abc import ABC

from src.router.route import Route


class RouterInterface(ABC):
    """
    Router interface
    """

    def add(self, route: Route) -> "RouterInterface":
        """
        Add route to collection

        :param route:
        :return:
        """

    def generate(self, name: str):
        """
        Search route by name and call it

        :param name:
        :return:
        """
