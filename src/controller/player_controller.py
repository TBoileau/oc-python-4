"""Imported modules/packages"""
from typing import List, Callable

from lib.controller.abstract_controller import AbstractController
from lib.helper.console import Console
from lib.input.input import Input
from lib.representation.header import Header
from lib.representation.representation import Representation

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
        players: List[Player] = self._entity_manager.get_repository(Player).find_all()

        representation: Representation = self._representation_factory.create()
        representation.add_header(Header(1, "Identifiant", lambda player: str(player.identifier)))
        representation.add_header(Header(2, "Genre", lambda player: player.gender))
        representation.add_header(Header(3, "Prénom", lambda player: player.first_name))
        representation.add_header(Header(4, "Nom", lambda player: player.last_name))
        representation.add_header(Header(5, "Date de naissance", lambda player: player.birthday.strftime("%d/%m/%Y")))
        representation.add_header(Header(6, "Classement", lambda player: str(player.ranking)))
        representation.set_data(players)
        representation.render()

        identifiers: List[str] = list(map(lambda player: str(player.identifier), players))

        input_: Input = Input(
            label="Saisissez l'identifiant d'un joueur que vous souhaitez sélectionner (R pour quitter) : ",
            message="Veuillez saisir R ou un identifiant parmi la liste.",
            validate=lambda raw_data: raw_data in ["R"] + identifiers,
        )

        def redirect_to_tournament(identifier: str) -> Callable:
            return lambda: self.redirect("player_update", [int(identifier)])

        self._choice(
            input_,
            {
                **{"R": lambda: self.redirect("app_home")},
                **dict(zip(identifiers, map(redirect_to_tournament, identifiers))),
            },
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
