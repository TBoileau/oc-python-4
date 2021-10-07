"""Imported modules/packages"""
import time

from src.controller.abstract_controller import AbstractController
from src.entity.tournament import Tournament
from src.form.tournament_form import TournamentForm
from src.gateway.tournament_gateway import TournamentGateway
from src.helper.console import Console
from src.router.router_interface import RouterInterface
from src.templating.templating_interface import TemplatingInterface


class TournamentController(AbstractController):
    """
    App controller
    """

    def __init__(self, templating: TemplatingInterface, router: RouterInterface, tournament_gateway: TournamentGateway):
        super().__init__(templating, router)
        self.__tournament_gateway: TournamentGateway = tournament_gateway

    def create(self):
        """
        Create tournament

        :return:
        """

        def handler(tournament: Tournament):
            self.__tournament_gateway.persist(tournament)
            Console.print("Tournois enregistré avec succès !", Console.SUCCESS)
            time.sleep(3)
            self.redirect("app_home")

        form: TournamentForm = TournamentForm(handler)
        self._form(form, "tournament/create")
