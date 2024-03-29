"""Imported modules/packages"""
from datetime import date
from typing import List, Dict, Any, Type

from tinydb.table import Document

from lib.orm.entity_manager_interface import EntityManagerInterface
from lib.orm.persistent import Persistent


class Player(Persistent):
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
        self.rank: float = 0
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
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthday": self.birthday.isoformat(),
            "gender": self.gender,
            "ranking": self.ranking,
        }

    @property
    def full_name(self) -> str:
        """
        Get full name

        :return:
        """
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def create(data: Document, entity_manager: EntityManagerInterface) -> "Player":
        return Player(
            identifier=data.doc_id,
            last_name=data["last_name"],
            first_name=data["first_name"],
            birthday=date.fromisoformat(data["birthday"]),
            gender=data["gender"],
            ranking=int(data["ranking"]),
        )

    @staticmethod
    def get_repository() -> Type:
        from src.repository.player_repository import PlayerRepository

        return PlayerRepository
