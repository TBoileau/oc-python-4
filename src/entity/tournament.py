"""Imported modules/packages"""
from datetime import datetime
from typing import Optional, List, Dict, Any

from src.entity.player import Player
from src.entity.round import Round
from src.serializer.serializable import Serializable
from src.workflow.subject import Subject
from src.workflow.transition import Transition


class Tournament(Serializable, Subject):
    """
    Tournament class
    """

    TYPE_BLITZ: str = "blitz"
    TYPE_SPEED: str = "speed"
    TYPE_BULLET: str = "bullet"

    def __init__(
        self,
        name: str,
        description: str,
        location: str,
        started_at: datetime,
        ended_at: Optional[datetime],
        time_control: str,
        number_of_rounds: int = 4,
        state: str = "pending",
        identifier: int = None,
        players: List[Player] = None,
        rounds: List[Round] = None,
    ):
        """
        Constructor

        :param name:
        :param description:
        :param location:
        :param started_at:
        :param ended_at:
        :param time_control:
        :param number_of_rounds:
        :param state:
        :param identifier:
        :param players:
        :param rounds:
        :param participants:
        """
        self.identifier: int = identifier
        self.name: str = name
        self.description: str = description
        self.location: str = location
        self.started_at: datetime = started_at
        self.ended_at: Optional[datetime] = ended_at
        self.players: List[Player] = players if players is not None else []
        self.rounds: List[Round] = rounds if rounds is not None else []
        self.time_control: str = time_control
        self.number_of_rounds: int = number_of_rounds
        self.__current_round_position: int = 0
        self.state: str = state

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

        self.generate_ranking()

        if self.__current_round_position > 0:
            assert self.current_round.ended
            self.current_round.end()

        self.__current_round_position += 1

        players: List[Player] = self.players

        self.rounds.append(Round(self.__current_round_position, players, []).start())

        return self

    def serialize(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "state": self.state,
            "description": self.description,
            "location": self.location,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at is not None else None,
            "time_control": self.time_control,
            "number_of_rounds": self.number_of_rounds,
            "rounds": list(map(lambda round_: round_.serialize(), self.rounds)),
            "players": list(map(lambda player: player.identifier, self.players)),
        }

    def get_state(self) -> str:
        return self.state

    def set_state(self, state: str):
        self.state = state

    def get_transitions(self) -> Dict[str, Transition]:
        return {
            "start": Transition(
                name="start",
                from_states=["pending"],
                to_state="started",
                guard=lambda tournament: len(tournament.players) > 0
                and len(tournament.players) > tournament.number_of_rounds > 0,
                completed=lambda tournament: tournament.start(),
            ),
            "finish": Transition("finish", ["started"], "finished"),
            "delete": Transition("delete", ["pending"], "deleted"),
        }

    def generate_ranking(self):
        """
        Generate ranking

        :return:
        """
        for player in self.players:
            player.points = 0
            player.opponents = []

        for round_ in self.rounds:
            for match in round_.matches:
                match.set_points()

        self.players.sort(key=lambda player: player.points, reverse=True)

        temp_player: Optional[Player] = None

        rank: int = 1

        for player in self.players:
            player.rank = rank if temp_player is None or temp_player.points != player.points else temp_player.rank
            temp_player = player
            rank += 1
