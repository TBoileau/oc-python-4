"""Imported modules/packages"""
import uuid
from datetime import datetime, date

import pytest

from src.entity.player import Player
from src.entity.tournament import Tournament


def test_tournament():
    tournament: Tournament = Tournament('Name', 'Description', 'Location', datetime.now(), None, Tournament.TYPE_BLITZ)

    with pytest.raises(AssertionError):
        tournament.start()

    player_1: Player = Player("1", "Player", date.today(), Player.GENDER_MALE, 1)
    player_2: Player = Player("2", "Player", date.today(), Player.GENDER_MALE, 2)
    player_3: Player = Player("3", "Player", date.today(), Player.GENDER_MALE, 3)
    player_4: Player = Player("4", "Player", date.today(), Player.GENDER_MALE, 4)
    player_5: Player = Player("5", "Player", date.today(), Player.GENDER_MALE, 5)
    player_6: Player = Player("6", "Player", date.today(), Player.GENDER_MALE, 6)
    player_7: Player = Player("7", "Player", date.today(), Player.GENDER_MALE, 7)
    player_8: Player = Player("8", "Player", date.today(), Player.GENDER_MALE, 8)

    tournament.register(player_1)

    with pytest.raises(AssertionError):
        tournament.start()

    tournament.register(player_2)
    tournament.register(player_3)
    tournament.register(player_4)
    tournament.register(player_5)
    tournament.register(player_6)
    tournament.register(player_7)
    tournament.register(player_8)

    tournament.start()

    assert "Round 1" == tournament.current_round.name

    with pytest.raises(AssertionError):
        tournament.new_round()

    assert len(tournament.players) == 8
    assert len(tournament.rounds) == 1

    assert tournament.current_round == tournament.current_round
    assert len(tournament.current_round.matches) == 4

    assert player_1 in tournament.current_round.matches[0].players and player_5 in tournament.current_round.matches[0].players
    with pytest.raises(AssertionError):
        tournament.current_round.matches[0].result(player_2)
    tournament.current_round.matches[0].result(player_1)
    assert player_1 == tournament.current_round.matches[0].winner
    assert player_1.points == 1
    assert player_5.points == 0

    assert player_2 in tournament.current_round.matches[1].players and player_6 in tournament.current_round.matches[1].players
    tournament.current_round.matches[1].result(player_2)
    assert player_2 == tournament.current_round.matches[1].winner
    assert player_2.points == 1
    assert player_6.points == 0

    assert player_3 in tournament.current_round.matches[2].players and player_7 in tournament.current_round.matches[2].players
    tournament.current_round.matches[2].result()
    assert tournament.current_round.matches[2].winner is None
    assert player_3.points == 0.5
    assert player_7.points == 0.5

    assert player_4 in tournament.current_round.matches[3].players and player_8 in tournament.current_round.matches[3].players
    tournament.current_round.matches[3].result(player_4)
    assert player_4 == tournament.current_round.matches[3].winner
    assert player_4.points == 1
    assert player_8.points == 0

    tournament.new_round()
    assert "Round 2" == tournament.current_round.name
    assert len(tournament.current_round.matches) == 4

    assert player_1 in tournament.current_round.matches[0].players and player_2 in tournament.current_round.matches[0].players
    tournament.current_round.matches[0].result(player_1)
    assert player_1 == tournament.current_round.matches[0].winner
    assert player_1.points == 2
    assert player_2.points == 1

    assert player_3 in tournament.current_round.matches[1].players and player_4 in tournament.current_round.matches[1].players
    tournament.current_round.matches[1].result(player_3)
    assert player_3 == tournament.current_round.matches[1].winner
    assert player_3.points == 1.5
    assert player_4.points == 1

    assert player_5 in tournament.current_round.matches[2].players and player_7 in tournament.current_round.matches[2].players
    tournament.current_round.matches[2].result()
    assert tournament.current_round.matches[2].winner is None
    assert player_5.points == 0.5
    assert player_7.points == 1

    assert player_6 in tournament.current_round.matches[3].players and player_8 in tournament.current_round.matches[3].players
    tournament.current_round.matches[3].result(player_6)
    assert player_6 == tournament.current_round.matches[3].winner
    assert player_6.points == 1
    assert player_8.points == 0

    tournament.new_round()
    assert "Round 3" == tournament.current_round.name
    assert len(tournament.current_round.matches) == 4

    assert player_1 in tournament.current_round.matches[0].players and player_3 in tournament.current_round.matches[0].players
    tournament.current_round.matches[0].result(player_1)
    assert player_1 == tournament.current_round.matches[0].winner
    assert player_1.points == 3
    assert player_3.points == 1.5

    assert player_2 in tournament.current_round.matches[1].players and player_4 in tournament.current_round.matches[1].players
    tournament.current_round.matches[1].result(player_2)
    assert player_2 == tournament.current_round.matches[1].winner
    assert player_2.points == 2
    assert player_4.points == 1

    assert player_6 in tournament.current_round.matches[2].players and player_7 in tournament.current_round.matches[2].players
    tournament.current_round.matches[2].result()
    assert tournament.current_round.matches[2].winner is None
    assert player_6.points == 1.5
    assert player_7.points == 1.5

    assert player_5 in tournament.current_round.matches[3].players and player_8 in tournament.current_round.matches[3].players
    tournament.current_round.matches[3].result(player_5)
    assert player_5 == tournament.current_round.matches[3].winner
    assert player_5.points == 1.5
    assert player_8.points == 0

    tournament.new_round()
    assert "Round 4" == tournament.current_round.name
    assert len(tournament.current_round.matches) == 4

    assert player_1 in tournament.current_round.matches[0].players and player_6 in tournament.current_round.matches[0].players
    tournament.current_round.matches[0].result(player_1)
    assert player_1 == tournament.current_round.matches[0].winner
    assert player_1.points == 4
    assert player_6.points == 1.5

    assert player_2 in tournament.current_round.matches[1].players and player_3 in tournament.current_round.matches[1].players
    tournament.current_round.matches[1].result(player_2)
    assert player_2 == tournament.current_round.matches[1].winner
    assert player_2.points == 3
    assert player_3.points == 1.5

    assert player_5 in tournament.current_round.matches[2].players and player_4 in tournament.current_round.matches[2].players
    tournament.current_round.matches[2].result()
    assert tournament.current_round.matches[2].winner is None
    assert player_5.points == 2
    assert player_4.points == 1.5

    assert player_7 in tournament.current_round.matches[3].players and player_8 in tournament.current_round.matches[3].players
    tournament.current_round.matches[3].result(player_7)
    assert player_7 == tournament.current_round.matches[3].winner
    assert player_7.points == 2.5
    assert player_8.points == 0

    with pytest.raises(AssertionError):
        tournament.new_round()

    assert True == tournament.ended
