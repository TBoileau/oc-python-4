"""Imported modules/packages"""
import copy
import random
from datetime import datetime
from typing import List, Optional, Dict, Any

from tinydb.table import Document

from lib.orm.entity import Entity
from lib.orm.entity_manager_interface import EntityManagerInterface
from lib.serializer.serializable import Serializable

from src.entity.match import Match
from src.entity.player import Player


class Round(Serializable, Entity):
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
        self.match_identifier: int = 1

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
        return len(self.matches) == len(list(filter(lambda match: match.ended, self.matches)))

    @property
    def pending_matches(self) -> List[Match]:
        """
        Get pending matches

        :return:
        """
        return [match for match in self.matches if match.ended is False]

    @property
    def finished_matches(self) -> List[Match]:
        """
        Get pending matches

        :return:
        """
        return [match for match in self.matches if match.ended is True]

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
        self.matches.append(Match(self.match_identifier, players[0], players[1]))
        self.match_identifier += 1

    def serialize(self) -> Dict[str, Any]:
        return {
            "position": self.position,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at is not None else None,
            "matches": list(map(lambda match: match.serialize(), self.matches)),
            "players": list(map(lambda player: player.identifier, self.players)),
        }

    @staticmethod
    def create(data: Document, entity_manager: EntityManagerInterface) -> "Round":
        return Round(
            position=int(data["position"]),
            started_at=datetime.fromisoformat(data["started_at"]),
            ended_at=datetime.fromisoformat(data["ended_at"]) if data["ended_at"] is not None else None,
            players=list(map(entity_manager.get_repository(Player).find, map(int, data["players"]))),
            matches=list(map(lambda match: Match.create(match, entity_manager), data["matches"])),
        )
