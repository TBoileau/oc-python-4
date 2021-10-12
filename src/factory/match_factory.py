"""Imported modules/packages"""

from tinydb.table import Document

from src.entity.match import Match
from src.factory.match_factory_interface import MatchFactoryInterface
from src.gateway.player_gateway import PlayerGateway


class MatchFactory(MatchFactoryInterface):
    """
    Match factory
    """

    def __init__(self, player_gateway: PlayerGateway):
        """
        Constructor

        :param player_gateway:
        """
        self.__player_gateway: PlayerGateway = player_gateway

    def create(self, data: Document) -> Match:
        return Match(
            identifier=int(data["identifier"]),
            white_player=self.__player_gateway.find(int(data["white_player"])),
            black_player=self.__player_gateway.find(int(data["black_player"])),
            winner=self.__player_gateway.find(int(data["winner"])) if data["winner"] is not None else None,
            ended=bool(data["ended"]),
        )
