"""Imported modules/packages"""
import os

from dotenv import load_dotenv
from tinydb import TinyDB

from src.controller.round_controller import RoundController
from src.controller.player_controller import PlayerController
from src.factory.match_factory import MatchFactory
from src.factory.match_factory_interface import MatchFactoryInterface
from src.factory.round_factory import RoundFactory
from src.factory.round_factory_interface import RoundFactoryInterface
from src.workflow.workflow import Workflow
from src.workflow.workflow_interface import WorkflowInterface
from src.factory.player_factory import PlayerFactory
from src.factory.player_factory_interface import PlayerFactoryInterface
from src.factory.tournament_factory import TournamentFactory
from src.factory.tournament_factory_interface import TournamentFactoryInterface
from src.representation.representation_factory import RepresentationFactory
from src.representation.representation_factory_interface import RepresentationFactoryInterface
from src.tinydb.tinydb_factory import TinyDBFactory
from src.controller.app_controller import AppController
from src.controller.tournament_controller import TournamentController
from src.dependency_injection.container import ContainerInterface, Container
from src.gateway.player_gateway import PlayerGateway
from src.gateway.tournament_gateway import TournamentGateway
from src.repository.player_repository import PlayerRepository
from src.repository.tournament_repository import TournamentRepository
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
        load_dotenv(f".env.{os.getenv('APP_ENV')}")
        self.build()
        self.routing()
        self.__container.get(Router).generate("app_home")

    def build(self):
        """
        Build container

        :return:
        """

        self.__container.set_parameter("templating_directory", os.path.join(os.getcwd(), "templates"))
        self.__container.set(TinyDB, TinyDBFactory.create(os.getenv("DB_URL")))
        self.__container.alias(TemplatingInterface, Templating)
        self.__container.alias(RouterInterface, Router)
        self.__container.alias(TournamentGateway, TournamentRepository)
        self.__container.alias(PlayerGateway, PlayerRepository)
        self.__container.alias(PlayerFactoryInterface, PlayerFactory)
        self.__container.alias(RoundFactoryInterface, RoundFactory)
        self.__container.alias(MatchFactoryInterface, MatchFactory)
        self.__container.alias(TournamentFactoryInterface, TournamentFactory)
        self.__container.alias(RepresentationFactoryInterface, RepresentationFactory)
        self.__container.alias(WorkflowInterface, Workflow)

    def routing(self):
        """
        Define routes

        :return:
        """
        router: RouterInterface = self.__container.get(RouterInterface)
        router.add(Route("app_home", AppController, "home"))
        router.add(Route("app_quit", AppController, "quit"))
        router.add(Route("tournament_create", TournamentController, "create"))
        router.add(Route("tournament_list", TournamentController, "list"))
        router.add(Route("tournament_read", TournamentController, "read"))
        router.add(Route("tournament_update", TournamentController, "update"))
        router.add(Route("tournament_players", TournamentController, "players"))
        router.add(Route("tournament_register", TournamentController, "register"))
        router.add(Route("tournament_unregister", TournamentController, "unregister"))
        router.add(Route("tournament_registration", TournamentController, "registration"))
        router.add(Route("tournament_start", TournamentController, "start"))
        router.add(Route("tournament_ranking", TournamentController, "ranking"))
        router.add(Route("player_list", PlayerController, "list"))
        router.add(Route("player_create", PlayerController, "create"))
        router.add(Route("player_update", PlayerController, "update"))
        router.add(Route("round_list", RoundController, "list"))
        router.add(Route("round_read", RoundController, "read"))
