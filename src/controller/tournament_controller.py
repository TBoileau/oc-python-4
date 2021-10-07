"""Imported modules/packages"""
import time
from typing import List, Callable

from src.controller.abstract_controller import AbstractController
from src.entity.tournament import Tournament
from src.form.tournament_form import TournamentForm
from src.gateway.tournament_gateway import TournamentGateway
from src.helper.console import Console
from src.input.input import Input
from src.representation.header import Header
from src.representation.representation import Representation
from src.representation.representation_factory_interface import RepresentationFactoryInterface
from src.router.router_interface import RouterInterface
from src.templating.templating_interface import TemplatingInterface


class TournamentController(AbstractController):
    """
    App controller
    """

    def __init__(
        self,
        templating: TemplatingInterface,
        router: RouterInterface,
        tournament_gateway: TournamentGateway,
        representation_factory: RepresentationFactoryInterface,
    ):
        super().__init__(templating, router)
        self.__tournament_gateway: TournamentGateway = tournament_gateway
        self.__representation_factory: RepresentationFactoryInterface = representation_factory

    def create(self):
        """
        Create tournament

        :return:
        """

        def handler(tournament: Tournament):
            self.__tournament_gateway.persist(tournament)
            Console.print("Tournois enregistré avec succès !", Console.SUCCESS)
            time.sleep(3)
            self.redirect("tournament_list")

        form: TournamentForm = TournamentForm(handler)
        self._form(form, "tournament/create")

    def list(self):
        """
        List tournaments

        :return:
        """
        tournaments: List[Tournament] = self.__tournament_gateway.find_all()

        representation: Representation = self.__representation_factory.create()
        representation.add_header(Header(1, "Identifiant", lambda tournament: str(tournament.identifier)))
        representation.add_header(Header(2, "Nom", lambda tournament: tournament.name))
        representation.add_header(Header(3, "Statut", lambda tournament: tournament.state))
        representation.set_data(tournaments)
        representation.render()

        identifiers: List[int] = list(map(lambda tournament: tournament.identifier, tournaments))

        input_: Input = Input(
            label="Saisissez l'identifiant du tournois que vous souhaitez sélectionner (0 pour quitter) : ",
            message="Veuillez saisir 0 ou un identifiant parmi la liste.",
            transform=int,
            validate=lambda raw_data: raw_data.isnumeric() and int(raw_data) in identifiers,
        )

        def redirect_to_tournament(tournament: Tournament) -> Callable:
            return lambda: self.redirect("tournament_read", [tournament.identifier])

        self._choice(
            input_,
            {
                **{0: lambda: self.redirect("home")},
                **dict(zip(map(redirect_to_tournament, tournaments), range(1, len(tournaments)))),
            },
        )

    def read(self, identifier):
        """
        Read tournament

        :param identifier:
        :return:
        """
