"""Imported modules/packages"""
from datetime import datetime

from tinydb.table import Document

from src.entity.round import Round
from src.factory.match_factory_interface import MatchFactoryInterface
from src.factory.round_factory_interface import RoundFactoryInterface
from src.gateway.player_gateway import PlayerGateway


class RoundFactory(RoundFactoryInterface):
    """
    Round factory
    """

    def __init__(self, player_gateway: PlayerGateway, match_factory: MatchFactoryInterface):
        """
        Constructor

        :param player_gateway:
        """
        self.__player_gateway: PlayerGateway = player_gateway
        self.__match_factory: MatchFactoryInterface = match_factory

    def create(self, data: Document) -> Round:
        return Round(
            position=int(data["position"]),
            started_at=datetime.fromisoformat(data["started_at"]),
            ended_at=datetime.fromisoformat(data["ended_at"]) if data["ended_at"] is not None else None,
            players=list(map(self.__player_gateway.find, map(int, data["players"]))),
            matches=list(map(self.__match_factory.create, data["matches"])),
        )
