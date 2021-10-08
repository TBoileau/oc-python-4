"""Imported modules/packages"""
from datetime import datetime

from tinydb.table import Document

from src.entity.match import Match
from src.entity.round import Round
from src.entity.tournament import Tournament
from src.factory.tournament_factory_interface import TournamentFactoryInterface
from src.gateway.player_gateway import PlayerGateway


class TournamentFactory(TournamentFactoryInterface):
    """
    Tournament factory
    """

    def __init__(self, player_gateway: PlayerGateway):
        """
        Constructor

        :param player_gateway:
        """
        self.__player_gateway: PlayerGateway = player_gateway

    def create(self, data: Document) -> Tournament:
        tournament: Tournament = Tournament(
            identifier=data.doc_id,
            name=data["name"],
            description=data["description"],
            location=data["location"],
            started_at=datetime.fromisoformat(data["started_at"]),
            ended_at=datetime.fromisoformat(data["ended_at"]) if data["ended_at"] is not None else None,
            time_control=data["time_control"],
            number_of_rounds=int(data["number_of_rounds"]),
        )

        for player_identifier in data["players"]:
            tournament.players.append(self.__player_gateway.find(int(player_identifier)))

        for round_raw in data["rounds"]:
            round_: Round = Round(
                int(round_raw["position"]),
                datetime.fromisoformat(round_raw["started_at"]),
                list(map(self.__player_gateway.find, round_raw["players"])),
            )

            for match_raw in round_raw["matches"]:
                match: Match = Match(
                    self.__player_gateway.find(match_raw["white_player"]),
                    self.__player_gateway.find(match_raw["black_player"]),
                )
                match.winner = self.__player_gateway.find(match_raw["winner"])
                match.ended = bool(match_raw["ended"])
                round_.matches.append(match)

            tournament.rounds.append(round_)

        return tournament
