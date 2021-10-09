"""Imported modules/packages"""
import io

import pytest
from dotenv import load_dotenv

from src.app import App

load_dotenv('.env.test')
stdin: str  = ""

def enter_input(input_: str):
    global stdin
    stdin += f'{input_}\n'

def test_app(capfd, monkeypatch):
    global stdin

    #Create tournament
    enter_input('1')
    enter_input('Tournois 2')
    enter_input('Description')
    enter_input('Paris')
    enter_input('1')
    enter_input('1')
    enter_input('01/01/2022 12:00')
    enter_input('10/01/2022 12:00')
    #Redirect to list tournaments
    #Show tournament 'Tournois 2'
    enter_input('2')
    #Update tournament 'Tournois 2'
    enter_input('M')
    enter_input('Tournois 2')
    enter_input('Description')
    enter_input('Paris')
    enter_input('1')
    enter_input('1')
    enter_input('01/01/2022 12:00')
    enter_input('10/01/2022 12:00')
    #Show tournament 'Tournois 2'
    #Registration player tournament 'Tournois 2'
    enter_input('I')
    #Register player 1
    enter_input('1')
    #Registration player tournament 'Tournois 2'
    #Register player 2
    enter_input('2')
    #Registration player tournament 'Tournois 2'
    #Register player 2
    enter_input('3')
    #Registration player tournament 'Tournois 2'
    #Return to list of players
    enter_input('R')
    #Delete player 3
    enter_input('3')
    #Return to show tournament 'Tournois 2'
    enter_input('R')
    #Start tournament 'Tournois 2'
    enter_input('D')
    #Return to show tournament 'Tournois 2'
    enter_input('R')
    #Return to home
    enter_input('0')
    #Quit
    enter_input('0')

    monkeypatch.setattr('sys.stdin', io.StringIO(stdin))

    with pytest.raises(SystemExit):
        app: App = App()
        app.run()
