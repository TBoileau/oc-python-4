"""Imported modules/packages"""
import copy
import random
from datetime import datetime
from typing import List, Optional, Dict, Any

from src.entity.match import Match
from src.entity.player import Player
from src.serializer.serializable import Serializable


class Round(Serializable):
    """
    Round class
    """

    def __init__(
        self,
        position: int,
        players: List[Player],
        matches: List[Match],
        started_at: Optional[datetime] = None,
        ended_at: Optional[datetime] = None,
    ):
        """
        Constructor

        :param position:
        :param started_at:
        :param players:
        :param matches:
        :param ended_at:
        """
        self.position: int = position
        self.started_at: Optional[datetime] = started_at
        self.ended_at: Optional[datetime] = ended_at
        self.players: List[Player] = players
        self.matches: List[Match] = matches

    def end(self) -> "Round":
        """
        End of round

        :return:
        """
        self.ended_at = datetime.now()

        return self

    @property
    def name(self) -> str:
        """
        Get name

        :return:
        """
        return f"Round {self.position}"

    @property
    def ended(self) -> bool:
        """
        Round is ended

        :return:
        """
        return len(self.players) // 2 == len(list(filter(lambda match: match.ended, self.matches)))

    @property
    def pending_matches(self) -> List[Match]:
        """
        Get pending matches

        :return:
        """
        return [match for match in self.matches if match.ended is None]

    @property
    def finished_matches(self) -> List[Match]:
        """
        Get pending matches

        :return:
        """
        return [match for match in self.matches if match.ended is not None]

    def start(self) -> "Round":
        """
        Start the round

        :return:
        """

        self.started_at = datetime.now()

        self.players.sort(key=lambda player: (player.points, len(self.players) - player.ranking), reverse=True)

        if self.position == 1:
            groups: List[List[Player]] = [
                self.players[: (len(self.players) // 2)],
                self.players[(len(self.players) // 2):],
            ]
            for i in range(0, len(groups[0])):
                self.__create_match([groups[0][i], groups[1][i]])

            return self

        players: List[Player] = copy.copy(self.players)

        while len(self.matches) < len(self.players) // 2:
            player = players[0]
            players.remove(player)
            potential_opponents: List[Player] = players
            for opponent in potential_opponents:
                if opponent not in player.opponents:
                    self.__create_match([player, opponent])
                    players.remove(opponent)
                    break

        return self

    def __create_match(self, players: List[Player]):
        """
        Create a new match

        :param players:
        :return:
        """
        random.shuffle(players)
        self.matches.append(Match(players[0], players[1]))

    def serialize(self) -> Dict[str, Any]:
        return {
            "position": self.position,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at is not None else None,
            "matches": list(map(lambda match: match.serialize(), self.matches)),
            "players": list(map(lambda player: player.identifier, self.players)),
        }
