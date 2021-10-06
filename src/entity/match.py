"""Imported modules/packages"""
from typing import Dict, Any, List, Optional

from src.entity.player import Player
from src.serializer.serializable import Serializable


class Match(Serializable):
    """
    Match class
    """

    def __init__(self, white_player: Player, black_player: Player):
        """
        Constructor

        :param white_player:
        :param black_player:
        """
        self.white_player: Player = white_player.play_against(black_player)
        self.black_player: Player = black_player.play_against(white_player)
        self.winner: Optional[Player] = None
        self.ended: bool = False

    @property
    def players(self) -> List[Player]:
        """
        Return list of players

        :return:
        """
        return [self.white_player, self.black_player]

    def result(self, winner: Optional[Player] = None) -> "Match":
        """
        Set result of the round

        :param winner:
        :return:
        """
        if winner is not None:
            assert winner in self.players
            self.winner = winner
            self.winner.points += 1
        else:
            self.white_player.points += 0.5
            self.black_player.points += 0.5

        self.ended = True

        return self

    def serialize(self) -> Dict[str, Any]:
        return {"white_player": self.white_player.id.__str__(), "black_player": self.black_player.id.__str__()}
