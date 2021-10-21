"""Imported modules/packages"""
from lib.controller.abstract_controller import AbstractController
from lib.helper.console import Console
from lib.representation.header import Header

from src.entity.player import Player
from src.form.player_form import PlayerForm


class PlayerController(AbstractController):
    """
    Player controller
    """

    def list(self):
        """
        List players

        :return:
        """
        self._list(
            headers=[
                Header(1, "Identifiant", lambda player: str(player.identifier)),
                Header(2, "Genre", lambda player: player.gender),
                Header(3, "Prénom", lambda player: player.first_name),
                Header(4, "Nom", lambda player: player.last_name),
                Header(5, "Date de naissance", lambda player: player.birthday.strftime("%d/%m/%Y")),
                Header(6, "Classement", lambda player: str(player.ranking)),
            ],
            data=self._entity_manager.get_repository(Player).find_all(),
            callback=lambda player: str(player.identifier),
            route="player_update",
            route_params=lambda identifier: [int(identifier)],
            backward="app_home",
        )

    def update(self, identifier: int):
        """
        Update player

        :param identifier:
        :return:
        """
        player: Player = self._entity_manager.get_repository(Player).find(identifier)

        def handler(player: Player):
            self._entity_manager.persist(player)
            Console.print("Joueur modifié avec succès !", Console.SUCCESS)
            self.redirect("player_list")

        form: PlayerForm = PlayerForm(handler, player)
        self._form(
            form,
            "player/update",
            {
                "identifier": player.identifier,
                "first_name": player.first_name,
                "last_name": player.last_name,
                "ranking": player.ranking,
                "gender": player.gender,
                "birthday": player.birthday.strftime("%d/%m/%Y %H:%M"),
            },
        )

    def create(self):
        """
        Create player

        :return:
        """

        def handler(player: Player):
            self._entity_manager.persist(player)
            Console.print("Joueur enregistré avec succès !", Console.SUCCESS)
            self.redirect("player_list")

        form: PlayerForm = PlayerForm(handler)
        self._form(form, "player/create")
