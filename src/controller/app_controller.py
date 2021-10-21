"""Imported modules/packages"""
import re
import sys

from lib.controller.abstract_controller import AbstractController
from lib.input.input import Input


class AppController(AbstractController):
    """
    App controller
    """

    def quit(self):
        """
        Quit program

        :return:
        """
        self.render("app/quit")
        sys.exit()

    def home(self):
        """
        Home

        :return:
        """
        home_input: Input = Input(
            label="Que souhaitez-vous faire ? ",
            message="Veuillez saisir un chiffre entre 0 et 3.",
            transform=int,
            validate=lambda raw_data: re.match(r"^\d+$", raw_data) and int(raw_data) in [0, 1, 2, 3, 4],
        )
        self._choice(
            home_input,
            {
                0: lambda: self.redirect("app_quit"),
                1: lambda: self.redirect("tournament_create"),
                2: lambda: self.redirect("tournament_list"),
                3: lambda: self.redirect("player_create"),
                4: lambda: self.redirect("player_list"),
            },
            "app/home",
        )
