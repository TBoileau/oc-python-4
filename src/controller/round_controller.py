"""Imported modules/packages"""
from typing import List, Callable

from src.controller.abstract_controller import AbstractController
from src.entity.round import Round
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

    def read(self, identifier: int, position: int):
        """
        Show round

        :param identifier:
        :param position:
        :return:
        """
        tournament: Tournament = self.__tournament_gateway.find(identifier)

        round_: Round = next(round_ for round_ in tournament.rounds if round_.position == position)

        representation: Representation = self.__representation_factory.create()
        representation.add_header(Header(1, "Identifier", lambda match: str(match.identifier)))
        representation.add_header(Header(2, "Statut", lambda match: "Terminé" if match.ended is True else "En cours"))
        representation.add_header(Header(3, "Joueur Blanc", lambda match: match.white_player.full_name))
        representation.add_header(
            Header(4, "", lambda match: ("V" if match.winner == match.white_player else "") if match.ended else "")
        )
        representation.add_header(
            Header(5, "", lambda match: ("N" if match.winner is None else "") if match.ended else "")
        )
        representation.add_header(
            Header(6, "", lambda match: ("V" if match.winner == match.black_player else "") if match.ended else "")
        )
        representation.add_header(Header(7, "Joueur Noir", lambda match: match.black_player.full_name))
        representation.set_data(round_.matches)
        representation.render()

        identifiers: List[str] = list(map(lambda match: str(match.identifier), round_.pending_matches))

        input_: Input = Input(
            label="Saisissez R pour retour ou l'identifier d'un match en cours pour saisir le résultat: ",
            message="Veuillez saisir R ou un identifiant.",
            validate=lambda raw_data: raw_data in ["R"] + identifiers,
        )

        def redirect_to_tournament(match_id: str) -> Callable:
            return lambda: self.redirect("match_result", [identifier, position, int(match_id)])

        self._choice(
            input_,
            {
                **{"R": lambda: self.redirect("round_list", [identifier])},
                **dict(zip(identifiers, map(redirect_to_tournament, identifiers))),
            },
        )

    def list(self, identifier: int):
        """
        List rounds

        :return:
        """
        tournament: Tournament = self.__tournament_gateway.find(identifier)

        representation: Representation = self.__representation_factory.create()
        representation.add_header(Header(1, "Nom", lambda round_: round_.name))
        representation.add_header(Header(2, "Matchs en cours", lambda round_: str(len(round_.pending_matches))))
        representation.add_header(Header(3, "Matchs terminés", lambda round_: str(len(round_.finished_matches))))
        representation.add_header(
            Header(4, "Statut", lambda round_: "Terminé" if round_.ended_at is not None else "En cours")
        )
        representation.set_data(tournament.rounds)
        representation.render()

        identifiers: List[str] = list(map(lambda round_: str(round_.position), tournament.rounds))

        input_: Input = Input(
            label="Saisissez l'identifiant d'une ronde que vous souhaitez sélectionner (R pour quitter) : ",
            message="Veuillez saisir R ou un identifiant parmi la liste.",
            validate=lambda raw_data: raw_data in ["R"] + identifiers,
        )

        def redirect_to_tournament(position: str) -> Callable:
            return lambda: self.redirect("round_read", [identifier, int(position)])

        self._choice(
            input_,
            {
                **{"R": lambda: self.redirect("tournament_read", [identifier])},
                **dict(zip(identifiers, map(redirect_to_tournament, identifiers))),
            },
        )
