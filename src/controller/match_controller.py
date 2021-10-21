"""Imported modules/packages"""
from lib.controller.abstract_controller import AbstractController
from lib.helper.console import Console
from lib.input.input import Input

from src.entity.match import Match
from src.entity.round import Round
from src.entity.tournament import Tournament


class MatchController(AbstractController):
    """
    Round controller
    """

    def result(self, identifier: int, position: int, match_identifier: int):
        """
        Set result to match

        :param identifier:
        :param position:
        :param match_identifier:
        :return:
        """
        tournament: Tournament = self._entity_manager.get_repository(Tournament).find(identifier)

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

        self._entity_manager.update(tournament)

        self.redirect("round_read", [identifier, tournament.current_round.position])
