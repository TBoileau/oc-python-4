"""Imported modules/packages"""
from datetime import date
from typing import List, Dict, Any

from src.serializer.serializable import Serializable


class Player(Serializable):
    """
    Player class
    """

    GENDER_MALE: str = "male"
    GENDER_FEMALE: str = "female"
    GENDER_NON_BINARY: str = "non binary"

    def __init__(
        self, last_name: str, first_name: str, birthday: date, gender: str, ranking: int, identifier: int = None
    ):
        """
        Constructor

        :param last_name:
        :param first_name:
        :param birthday:
        :param gender:
        :param ranking:
        :param identifier:
        """
        self.last_name: str = last_name
        self.first_name: str = first_name
        self.birthday: date = birthday
        self.gender: str = gender
        self.ranking: int = ranking
        self.points: float = 0
        self.opponents: List["Player"] = []
        self.identifier: int = identifier

    def play_against(self, opponent: "Player") -> "Player":
        """
        Play against an opponent

        :param opponent:
        :return:
        """
        self.opponents.append(opponent)

        return self

    def serialize(self) -> Dict[str, Any]:
        return {
            "id": self.identifier,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthday": self.birthday.isoformat(),
            "gender": self.gender,
            "ranking": self.ranking,
        }
