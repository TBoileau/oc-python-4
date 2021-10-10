"""Imported modules/packages"""
from datetime import datetime

from tinydb.table import Document

from src.entity.tournament import Tournament
from src.factory.round_factory_interface import RoundFactoryInterface
from src.factory.tournament_factory_interface import TournamentFactoryInterface
from src.gateway.player_gateway import PlayerGateway


class TournamentFactory(TournamentFactoryInterface):
    """
    Tournament factory
    """

    def __init__(self, player_gateway: PlayerGateway, round_factory: RoundFactoryInterface):
        """
        Constructor

        :param player_gateway:
        """
        self.__player_gateway: PlayerGateway = player_gateway
        self.__round_factory: RoundFactoryInterface = round_factory

    def create(self, data: Document) -> Tournament:
        return Tournament(
            identifier=data.doc_id,
            name=data["name"],
            description=data["description"],
            state=data["state"],
            location=data["location"],
            started_at=datetime.fromisoformat(data["started_at"]),
            ended_at=datetime.fromisoformat(data["ended_at"]) if data["ended_at"] is not None else None,
            time_control=data["time_control"],
            number_of_rounds=int(data["number_of_rounds"]),
            players=list(map(lambda player: self.__player_gateway.find(int(player)), data["players"])),
            rounds=list(map(self.__round_factory.create, data["rounds"])),
        )
