"""Imported modules/packages"""
import os
from abc import ABC

from dotenv import load_dotenv

from lib.dependency_injection.container import ContainerInterface, Container
from lib.router.router_interface import RouterInterface


class Kernel(ABC):
    """
    Kernel class
    """

    def __init__(self):
        self.__container: ContainerInterface = Container()
        load_dotenv(".env")
        load_dotenv(f".env.{os.getenv('APP_ENV')}")

    def run(self):
        """
        Run app

        :return:
        """
        self.build(self.__container)
        self.routing(self.__container.get(RouterInterface))
        self.start(self.__container.get(RouterInterface))

    def start(self, router: RouterInterface):
        """
        Start app

        :return:
        """

    def build(self, container: ContainerInterface):
        """
        Build container

        :return:
        """

    def routing(self, router: RouterInterface):
        """
        Define routes

        :return:
        """
