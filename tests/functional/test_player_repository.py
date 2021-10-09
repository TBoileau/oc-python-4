"""Imported modules/packages"""
import uuid
from datetime import date
from os import getenv

import pytest
from dotenv import load_dotenv
from tinydb import TinyDB

from src.entity.player import Player
from src.factory.player_factory import PlayerFactory, PlayerFactoryInterface
from src.gateway.player_gateway import PlayerGateway
from src.repository.player_repository import PlayerRepository
from src.tinydb.tinydb_factory import TinyDBFactory


load_dotenv('.env.test')
tiny_db: TinyDB = TinyDBFactory.create(getenv('DB_URL'))

def test_find():
    player_factory: PlayerFactoryInterface = PlayerFactory()
    player_repository: PlayerGateway = PlayerRepository(tiny_db, player_factory)
    assert player_repository.find(0) is None
    assert player_repository.find(1) is not None

def test_find_all():
    player_factory: PlayerFactoryInterface = PlayerFactory()
    player_repository: PlayerGateway = PlayerRepository(tiny_db, player_factory)
    assert len(player_repository.find_all()) == 8

def test_persist():
    player_factory: PlayerFactoryInterface = PlayerFactory()
    player_repository: PlayerGateway = PlayerRepository(tiny_db, player_factory)
    player: Player = Player('Doe', 'John', date.today(), Player.GENDER_MALE, 1)
    player_repository.persist(player)
    assert len(player_repository.find_all()) == 9
    assert player_repository.find(player.identifier) is not None
