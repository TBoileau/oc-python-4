"""Imported modules/packages"""
import os

from dotenv import load_dotenv

from src.controller.app_controller import AppController
from src.controller.tournament_controller import TournamentController
from src.dependency_injection.container import ContainerInterface, Container
from src.router.route import Route
from src.router.router import Router
from src.router.router_interface import RouterInterface
from src.templating.templating import Templating
from src.templating.templating_interface import TemplatingInterface


class App:
    """
    App class
    """

    def __init__(self):
        self.__container: ContainerInterface = Container()

    def run(self):
        """
        Run app

        :return:
        """

        load_dotenv(".env")
        self.build()
        self.routing()
        self.__container.get(Router).generate("app_home")

    def build(self):
        """
        Build container

        :return:
        """

        self.__container.set_parameter("templating_directory", os.path.join(os.getcwd(), "templates")).alias(
            TemplatingInterface, Templating
        ).alias(RouterInterface, Router)

    def routing(self):
        """
        Define routes

        :return:
        """

        self.__container.get(RouterInterface).add(Route("app_home", AppController, "home")).add(
            Route("app_quit", AppController, "quit")
        ).add(Route("tournament_create", TournamentController, "create"))
