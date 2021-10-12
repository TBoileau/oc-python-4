"""Imported modules/packages"""
from src.controller.abstract_controller import AbstractController
from src.entity.match import Match
from src.entity.round import Round
from src.entity.tournament import Tournament
from src.gateway.tournament_gateway import TournamentGateway
from src.helper.console import Console
from src.input.input import Input
from src.router.router_interface import RouterInterface
from src.templating.templating_interface import TemplatingInterface


class MatchController(AbstractController):
    """
    Round controller
    """

    def __init__(
        self,
        templating: TemplatingInterface,
        router: RouterInterface,
        tournament_gateway: TournamentGateway,
    ):
        super().__init__(templating, router)
        self.__tournament_gateway: TournamentGateway = tournament_gateway

    def result(self, identifier: int, position: int, match_identifier: int):
        """
        Set result to match

        :param identifier:
        :param position:
        :param match_identifier:
        :return:
        """
        tournament: Tournament = self.__tournament_gateway.find(identifier)

        round_: Round = next(round_ for round_ in tournament.rounds if round_.position == position)

        match: Match = next(match for match in round_.pending_matches if match.identifier == match_identifier)

        input_: Input = Input(
            label="Qui a gagné ? B pour le joueur Blanc, N pour le joueur Noir et E pour une égalité ou R pour retour",
            message="Veuillez saisir R, B, N ou E.",
            validate=lambda raw_data: raw_data in ["R", "N", "E", "B"],
        )

        self._choice(
            input_,
            {
                "R": lambda: self.redirect("round_read", [identifier, position]),
                "B": lambda: match.result(match.white_player),
                "N": lambda: match.result(match.black_player),
                "E": match.result,
            },
        )

        Console.print("Match terminé.", Console.SUCCESS)

        if len(round_.pending_matches) == 0:
            tournament.new_round()

        self.__tournament_gateway.update(tournament)

        self.redirect("round_read", [identifier, tournament.current_round.position])
