"""Imported modules/packages"""
from src.controller.abstract_controller import AbstractController


class AppController(AbstractController):
    """
    App controller
    """

    def home(self):
        """
        Home

        :return:
        """
        self._render("home")
        self.redirect("Que souhaitez-vous faire ?", {0: exit})
