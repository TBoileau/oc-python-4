"""Imported modules/packages"""
from typing import List

from src.controller.abstract_controller import AbstractController
from src.entity.player import Player
from src.form.player_form import PlayerForm
from src.gateway.player_gateway import PlayerGateway
from src.helper.console import Console
from src.input.input import Input
from src.representation.header import Header
from src.representation.representation import Representation
from src.representation.representation_factory_interface import RepresentationFactoryInterface
from src.router.router_interface import RouterInterface
from src.templating.templating_interface import TemplatingInterface


class PlayerController(AbstractController):
    """
    Player controller
    """

    def __init__(
        self,
        templating: TemplatingInterface,
        router: RouterInterface,
        player_gateway: PlayerGateway,
        representation_factory: RepresentationFactoryInterface,
    ):
        super().__init__(templating, router)
        self.__player_gateway: PlayerGateway = player_gateway
        self.__representation_factory: RepresentationFactoryInterface = representation_factory

    def list(self):
        """
        Liste players

        :return:
        """
        players: List[Player] = self.__player_gateway.find_all()

        representation: Representation = self.__representation_factory.create()
        representation.add_header(Header(1, "Identifiant", lambda player: str(player.identifier)))
        representation.add_header(Header(2, "Prénom", lambda player: player.first_name))
        representation.add_header(Header(3, "Nom", lambda player: player.last_name))
        representation.add_header(Header(4, "Rang", lambda player: str(player.ranking)))
        representation.set_data(players)
        representation.render()

        input_: Input = Input(
            label="Saisissez R pour retour ou C pour créer un nouveau joueur : ",
            message="Veuillez saisir R ou C.",
            validate=lambda raw_data: raw_data in ["R", "C"],
        )

        self._choice(
            input_,
            {
                "R": lambda: self.redirect("app_home"),
                "C": lambda: self.redirect("player_create"),
            },
        )

    def create(self):
        """
        Create player

        :return:
        """
        def handler(player: Player):
            self.__player_gateway.persist(player)
            Console.print("Joueur enregistré avec succès !", Console.SUCCESS)
            self.redirect("player_list")

        form: PlayerForm = PlayerForm(handler)
        self._form(form, "player/create")
