"""Imported modules/packages"""
from typing import Dict, Any, List, Optional

from tinydb.table import Document

from lib.orm.entity import Entity
from lib.orm.entity_manager_interface import EntityManagerInterface
from lib.serializer.serializable import Serializable

from src.entity.player import Player


class Match(Serializable, Entity):
    """
    Match class
    """

    def __init__(
        self,
        identifier: int,
        white_player: Player,
        black_player: Player,
        winner: Optional[Player] = None,
        ended: bool = False,
    ):
        """
        Constructor

        :param identifier:
        :param white_player:
        :param black_player:
        :param winner:
        :param ended:
        """
        self.identifier: int = identifier
        self.white_player: Player = white_player.play_against(black_player)
        self.black_player: Player = black_player.play_against(white_player)
        self.winner: Optional[Player] = winner
        self.ended: bool = ended

    @property
    def players(self) -> List[Player]:
        """
        Return list of players

        :return:
        """
        return [self.white_player, self.black_player]

    def set_points(self):
        """
        Set points of white and black players

        :return:
        """
        self.white_player.play_against(self.black_player)
        self.black_player.play_against(self.white_player)

        if self.ended:
            if self.winner is not None:
                self.winner.points += 1
            else:
                self.white_player.points += 0.5
                self.black_player.points += 0.5

    def result(self, winner: Optional[Player] = None) -> "Match":
        """
        Set result of the round

        :param winner:
        :return:
        """

        if winner is not None:
            assert winner in self.players
            self.winner = winner

        self.ended = True

        self.set_points()

        return self

    def serialize(self) -> Dict[str, Any]:
        return {
            "identifier": self.identifier,
            "white_player": self.white_player.identifier,
            "black_player": self.black_player.identifier,
            "winner": self.winner.identifier if self.winner is not None else None,
            "ended": self.ended,
        }

    @staticmethod
    def create(data: Document, entity_manager: EntityManagerInterface) -> "Match":
        return Match(
            identifier=int(data["identifier"]),
            white_player=entity_manager.get_repository(Player).find(int(data["white_player"])),
            black_player=entity_manager.get_repository(Player).find(int(data["black_player"])),
            winner=entity_manager.get_repository(Player).find(int(data["winner"]))
            if data["winner"] is not None
            else None,
            ended=bool(data["ended"]),
        )
