"""Imported modules/packages"""
from lib.controller.abstract_controller import AbstractController
from lib.representation.header import Header

from src.entity.round import Round
from src.entity.tournament import Tournament


class RoundController(AbstractController):
    """
    Round controller
    """

    def read(self, tournament_identifier: int, position: int):
        """
        Show round

        :param tournament_identifier:
        :param position:
        :return:
        """
        tournament: Tournament = self._entity_manager.get_repository(Tournament).find(tournament_identifier)

        round_: Round = next(round_ for round_ in tournament.rounds if round_.position == position)

        self._list(
            headers=[
                Header(1, "Identifier", lambda match: str(match.identifier)),
                Header(2, "Statut", lambda match: "Terminé" if match.ended is True else "En cours"),
                Header(3, "Joueur Blanc", lambda match: match.white_player.full_name),
                Header(4, "", lambda match: ("V" if match.winner == match.white_player else "") if match.ended else ""),
                Header(5, "", lambda match: ("N" if match.winner is None else "") if match.ended else ""),
                Header(6, "", lambda match: ("V" if match.winner == match.black_player else "") if match.ended else ""),
                Header(7, "Joueur Noir", lambda match: match.black_player.full_name),
            ],
            data=round_.matches,
            callback=lambda match: str(match.identifier),
            route="match_result",
            route_params=lambda identifier: [tournament_identifier, position, int(identifier)],
            backward="round_list",
            backward_params=[tournament_identifier],
        )

    def list(self, tournament_identifier: int):
        """
        List rounds

        :return:
        """
        self._list(
            headers=[
                Header(1, "Nom", lambda round_: round_.name),
                Header(2, "Matchs en cours", lambda round_: str(len(round_.pending_matches))),
                Header(3, "Matchs terminés", lambda round_: str(len(round_.finished_matches))),
                Header(4, "Statut", lambda round_: "Terminé" if round_.ended_at is not None else "En cours"),
            ],
            data=self._entity_manager.get_repository(Tournament).find(tournament_identifier).rounds,
            callback=lambda round_: str(round_.position),
            route="round_read",
            route_params=lambda position: [tournament_identifier, int(position)],
            backward="tournament_read",
            backward_params=[tournament_identifier],
        )
