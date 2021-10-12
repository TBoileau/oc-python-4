"""Imported modules/packages"""
from typing import List, Callable

from src.controller.abstract_controller import AbstractController
from src.entity.tournament import Tournament
from src.gateway.tournament_gateway import TournamentGateway
from src.input.input import Input
from src.representation.header import Header
from src.representation.representation import Representation
from src.representation.representation_factory_interface import RepresentationFactoryInterface
from src.router.router_interface import RouterInterface
from src.templating.templating_interface import TemplatingInterface


class RoundController(AbstractController):
    """
    Round controller
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

    def list(self, identifier: int):
        """
        List rounds

        :return:
        """
        tournament: Tournament = self.__tournament_gateway.find(identifier)

        representation: Representation = self.__representation_factory.create()
        representation.add_header(Header(1, "Nom", lambda round: round.name))
        representation.add_header(Header(2, "Matchs en cours", lambda round: str(len(round.pending_matches))))
        representation.add_header(Header(3, "Matchs terminés", lambda round: str(len(round.finished_matches))))
        representation.add_header(
            Header(4, "Statut", lambda round: "Terminé" if round.ended_at is not None else "En cours")
        )
        representation.set_data(tournament.rounds)
        representation.render()

        identifiers: List[str] = list(map(lambda round: str(round.position), tournament.rounds))

        input_: Input = Input(
            label="Saisissez l'identifiant d'une ronde que vous souhaitez sélectionner (R pour quitter) : ",
            message="Veuillez saisir R ou un identifiant parmi la liste.",
            validate=lambda raw_data: raw_data in ["R"] + identifiers,
        )

        def redirect_to_tournament(round_id: str) -> Callable:
            return lambda: self.redirect("round_read", [identifier, int(round_id)])

        self._choice(
            input_,
            {
                **{"R": lambda: self.redirect("tournament_read", [identifier])},
                **dict(zip(identifiers, map(redirect_to_tournament, identifiers))),
            },
        )
