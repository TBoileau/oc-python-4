"""Imported modules/packages"""
from abc import ABC
from typing import List, Any

from lib.router.route import Route


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

    def generate(self, name: str, params: List[Any] = None):
        """
        Search route by name and call it

        :param name:
        :param params:
        :return:
        """
