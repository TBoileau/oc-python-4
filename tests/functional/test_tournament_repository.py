"""Imported modules/packages"""
import uuid
from datetime import datetime
from os import getenv

import pytest
from dotenv import load_dotenv
from tinydb import TinyDB

from src.entity.tournament import Tournament
from src.factory.player_factory import PlayerFactory, PlayerFactoryInterface
from src.factory.tournament_factory import TournamentFactoryInterface, TournamentFactory
from src.gateway.player_gateway import PlayerGateway
from src.gateway.tournament_gateway import TournamentGateway
from src.repository.player_repository import PlayerRepository
from src.repository.tournament_repository import TournamentRepository
from src.tinydb.tinydb_factory import TinyDBFactory


load_dotenv('.env.test')
tiny_db: TinyDB = TinyDBFactory.create(getenv('DB_URL'))

def test_find():
    player_factory: PlayerFactoryInterface = PlayerFactory()
    player_repository: PlayerGateway = PlayerRepository(tiny_db, player_factory)
    tournament_factory: TournamentFactoryInterface = TournamentFactory(player_repository)
    tournament_repository: TournamentGateway = TournamentRepository(tiny_db, tournament_factory)
    assert tournament_repository.find('fail') is None
    assert tournament_repository.find('8c265135-c6a6-4652-897a-ec02b787a41d') is not None

def test_find_all():
    player_factory: PlayerFactoryInterface = PlayerFactory()
    player_repository: PlayerGateway = PlayerRepository(tiny_db, player_factory)
    tournament_factory: TournamentFactoryInterface = TournamentFactory(player_repository)
    tournament_repository: TournamentGateway = TournamentRepository(tiny_db, tournament_factory)
    assert len(tournament_repository.find_all()) == 1

def test_persist():
    player_factory: PlayerFactoryInterface = PlayerFactory()
    player_repository: PlayerGateway = PlayerRepository(tiny_db, player_factory)
    tournament_factory: TournamentFactoryInterface = TournamentFactory(player_repository)
    tournament_repository: TournamentGateway = TournamentRepository(tiny_db, tournament_factory)
    tournament: Tournament = Tournament(uuid.uuid4(), 'Tournament', 'Description', 'Paris', datetime.now(), None, Tournament.TYPE_BLITZ)
    tournament.register(player_repository.find('6f6891be-a71a-47c5-8253-d9c0e583e6bd'))
    tournament_repository.persist(tournament)
    assert len(tournament_repository.find_all()) == 2
    assert tournament_repository.find(tournament.identifier.__str__()) is not None