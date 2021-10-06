"""Imported modules/packages"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from src.entity.player import Player
from src.entity.round import Round
from src.serializer.serializable import Serializable


class Tournament(Serializable):
    """
    Tournament class
    """

    TYPE_BLITZ: str = "blitz"
    TYPE_SPEED: str = "speed"
    TYPE_BULLET: str = "bullet"

    def __init__(
        self,
        identifier: UUID,
        name: str,
        description: str,
        location: str,
        started_at: datetime,
        ended_at: Optional[datetime],
        time_control: str,
        number_of_rounds: int = 4,
    ):
        """
        Constructor

        :param identifier:
        :param name:
        :param description:
        :param location:
        :param started_at:
        :param ended_at:
        :param time_control:
        :param number_of_rounds:
        """
        self.identifier: UUID = identifier
        self.name: str = name
        self.description: str = description
        self.location: str = location
        self.started_at: datetime = started_at
        self.ended_at: Optional[datetime] = ended_at
        self.players: List[Player] = []
        self.rounds: List[Round] = []
        self.time_control: str = time_control
        self.number_of_rounds: int = number_of_rounds
        self.__current_round_position: int = 0

    def register(self, player: Player) -> "Tournament":
        """
        Register a player to the tournament

        :param player:
        :return:
        """
        self.players.append(player)

        return self

    def start(self) -> "Tournament":
        """
        Start the tournament

        :return:
        """
        assert len(self.players) > 0
        assert len(self.players) % 2 == 0

        return self.new_round()

    @property
    def ended(self) -> bool:
        """
        Check if tournament is done

        :return:
        """
        return self.number_of_rounds == self.__current_round_position

    @property
    def current_round(self) -> Round:
        """
        Return current round

        :return:
        """
        return self.rounds[self.__current_round_position - 1]

    def new_round(self) -> "Tournament":
        """
        New round

        :return:
        """
        assert self.__current_round_position < self.number_of_rounds

        if self.__current_round_position > 0:
            assert self.current_round.ended
            self.current_round.end()

        self.__current_round_position += 1

        players: List[Player] = self.players

        self.rounds.append(Round(self.__current_round_position, datetime.now(), players).start())

        return self

    def serialize(self) -> Dict[str, Any]:
        return {
            "id": self.identifier.__str__(),
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at is not None else None,
            "time_control": self.time_control,
            "number_of_rounds": self.number_of_rounds,
            "rounds": list(map(lambda round_: round_.serialize(), self.rounds)),
            "players": list(map(lambda player: player.identifier.__str__(), self.players)),
        }
