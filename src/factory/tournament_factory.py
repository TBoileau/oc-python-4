"""Imported modules/packages"""
from abc import ABC
from datetime import datetime
from typing import Dict
from uuid import UUID

from src.entity.match import Match
from src.entity.round import Round
from src.entity.tournament import Tournament
from src.gateway.player_gateway import PlayerGateway


class TournamentFactoryInterface(ABC):
    """
    Tournament factory interface
    """

    def create(self, data: Dict) -> Tournament:
        """
        Create an instance of Tournament

        :param data:
        :return:
        """


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

    def create(self, data: Dict) -> Tournament:
        tournament: Tournament = Tournament(
            UUID(data["id"]),
            data["name"],
            data["description"],
            data["location"],
            datetime.fromisoformat(data["started_at"]),
            datetime.fromisoformat(data["ended_at"]) if data["ended_at"] is not None else None,
            data["time_control"],
            int(data["number_of_rounds"]),
        )

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
