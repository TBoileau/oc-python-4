"""Imported modules/packages"""
from lib.kernel import Kernel
from lib.router.route import Route
from lib.router.router_interface import RouterInterface

from src.controller.match_controller import MatchController
from src.controller.round_controller import RoundController
from src.controller.player_controller import PlayerController
from src.controller.app_controller import AppController
from src.controller.tournament_controller import TournamentController


class AppKernel(Kernel):
    """
    AppKernel class
    """

    def start(self, router: RouterInterface):
        router.generate("app_home")

    def routing(self, router: RouterInterface):
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
        router.add(Route("match_result", MatchController, "result"))
