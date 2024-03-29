"""Imported modules/packages"""
import io

import pytest
from dotenv import load_dotenv

from src.app_kernel import AppKernel

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
    #Return to tournament
    enter_input('R')
    #Lst of players
    enter_input('J')
    #Delete player 3
    enter_input('3')
    #Return to show tournament 'Tournois 2'
    enter_input('R')
    #Start tournament 'Tournois 2'
    enter_input('D')
    #Return to show tournament 'Tournois 2'
    #List of rounds
    enter_input('T')
    #Show round 1
    enter_input('1')
    #Set result of match 1
    enter_input('1')
    #Set winner Black
    enter_input('B')
    #Return to show round 1
    #Return to list of rounds
    enter_input('R')
    #Return to show tournament 'Tournois 2'
    enter_input('R')
    #Return to tournaments list
    enter_input('R')
    #Show 'Tournois 1'
    enter_input('1')
    #Ranking 'Tournois 2'
    enter_input('C')
    #Return to show tournament 'Tournois 1'
    enter_input('R')
    #Show rounds
    enter_input('T')
    #Show first round
    enter_input('1')
    #Return to list of rounds
    enter_input('R')
    #Return to show tournament 'Tournois 1'
    enter_input('R')
    #Return to tournaments list
    enter_input('R')
    #Return to home
    enter_input('R')
    #List players
    enter_input('4')
    #Return to home
    enter_input('R')
    #Create player
    enter_input('3')
    enter_input('Thomas')
    enter_input('Boileau')
    enter_input('H')
    enter_input('17/09/1988')
    enter_input('1')
    #Return to players list
    enter_input('1')
    enter_input('Thomas')
    enter_input('Boileau')
    enter_input('H')
    enter_input('17/09/1988')
    enter_input('1')
    #Return to players list
    #Go to home
    enter_input('R')
    #Quit
    enter_input('0')

    monkeypatch.setattr('sys.stdin', io.StringIO(stdin))

    with pytest.raises(SystemExit):
        app: AppKernel = AppKernel()
        app.run()
