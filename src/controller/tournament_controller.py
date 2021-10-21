"""Imported modules/packages"""
from typing import List

from lib.controller.abstract_controller import AbstractController
from lib.helper.console import Console
from lib.input.input import Input
from lib.representation.header import Header

from src.entity.player import Player
from src.entity.tournament import Tournament
from src.form.tournament_form import TournamentForm


class TournamentController(AbstractController):
    """
    App controller
    """

    def create(self):
        """
        Create tournament

        :return:
        """

        def handler(tournament: Tournament):
            self._entity_manager.persist(tournament)
            Console.print("Tournois enregistré avec succès !", Console.SUCCESS)
            self.redirect("tournament_list")

        form: TournamentForm = TournamentForm(handler)
        self._form(form, "tournament/create")

    def unregister(self, identifier: int, player_id: int):
        """
        Unregister player from tournament
        :param identifier:
        :param player_id:
        :return:
        """
        tournament: Tournament = self._entity_manager.get_repository(Tournament).find(identifier)

        if tournament.get_state() != "pending":
            Console.print("Vous ne pouvez pas inscrire un joueur alors dans un tournois commencé.", Console.FAIL)
            self.redirect("tournament_players", [identifier])
            return

        if player_id not in list(map(lambda player: player.identifier, tournament.players)):
            Console.print("Ce joueur n'est pas inscrit au tournois.", Console.FAIL)
            self.redirect("tournament_players", [identifier])
            return

        player: Player = next(player for player in tournament.players if player.identifier == player_id)

        tournament.players.remove(player)

        self._entity_manager.update(tournament)

        Console.print("Joueur désinscrit avec succès.", Console.SUCCESS)

        self.redirect("tournament_players", [identifier])

    def register(self, identifier: int, player_id: int):
        """
        Register player from tournament
        :param identifier:
        :param player_id:
        :return:
        """
        tournament: Tournament = self._entity_manager.get_repository(Tournament).find(identifier)

        player: Player = self._entity_manager.get_repository(Player).find(player_id)

        tournament.players.append(player)

        self._entity_manager.update(tournament)

        Console.print("Joueur inscrit avec succès.", Console.SUCCESS)

        self.redirect("tournament_registration", [identifier])

    def players(self, tournament_identifier: int):
        """
        List tournaments players
        :param tournament_identifier:
        :return:
        """
        tournament: Tournament = self._entity_manager.get_repository(Tournament).find(tournament_identifier)

        self._list(
            headers=[
                Header(1, "Identifiant", lambda player: str(player.identifier)),
                Header(2, "Nom", lambda player: f"{player.first_name} {player.last_name}"),
            ],
            data=tournament.players,
            callback=lambda player: str(player.identifier),
            route="tournament_unregister",
            route_params=lambda identifier: [tournament_identifier, int(identifier)],
            backward="tournament_read",
            backward_params=[tournament_identifier],
        )

    def registration(self, tournament_identifier: int):
        """
        Registration player in tournament
        :param tournament_identifier:
        :return:
        """
        tournament: Tournament = self._entity_manager.get_repository(Tournament).find(tournament_identifier)

        if tournament.get_state() != "pending":
            Console.print("Vous ne pouvez pas inscrire un joueur alors dans un tournois commencé.", Console.FAIL)

        players: List[Player] = [
            player
            for player in self._entity_manager.get_repository(Player).find_all()
            if player not in tournament.players
        ]

        self._list(
            headers=[
                Header(1, "Identifiant", lambda player: str(player.identifier)),
                Header(2, "Nom", lambda player: f"{player.first_name} {player.last_name}"),
            ],
            data=players,
            callback=lambda player: str(player.identifier),
            route="tournament_register",
            route_params=lambda identifier: [tournament_identifier, int(identifier)],
            backward="tournament_read",
            backward_params=[tournament_identifier],
        )

    def list(self):
        """
        List tournaments

        :return:
        """
        self._list(
            headers=[
                Header(1, "Identifiant", lambda tournament: str(tournament.identifier)),
                Header(2, "Nom", lambda tournament: tournament.name),
                Header(3, "Statut", lambda tournament: tournament.state),
            ],
            data=self._entity_manager.get_repository(Tournament).find_all(),
            callback=lambda tournament: str(tournament.identifier),
            route="tournament_read",
            route_params=lambda identifier: [int(identifier)],
            backward="app_home",
        )

    def read(self, identifier: int):
        """
        Read tournament

        :param identifier:
        :return:
        """

        input_: Input = Input(
            label="Que souhaitez-vous faire ? ",
            message="Veuillez saisir un action.",
            transform=str,
            validate=lambda raw_data: raw_data in ["R", "J", "I", "M", "D", "C", "T"],
        )

        tournament: Tournament = self._entity_manager.get_repository(Tournament).find(identifier)

        self._choice(
            input_,
            {
                "R": lambda: self.redirect("tournament_list"),
                "J": lambda: self.redirect("tournament_players", [identifier]),
                "M": lambda: self.redirect("tournament_update", [identifier]),
                "D": lambda: self.redirect("tournament_start", [identifier]),
                "I": lambda: self.redirect("tournament_registration", [identifier]),
                "C": lambda: self.redirect("tournament_ranking", [identifier]),
                "T": lambda: self.redirect("round_list", [identifier]),
            },
            "tournament/read",
            {
                "identifier": tournament.identifier,
                "name": tournament.name,
                "state": tournament.state,
                "description": tournament.description,
                "location": tournament.location,
                "started_at": tournament.started_at.strftime("%d/%m/%Y %H:%M"),
                "ended_at": tournament.ended_at.strftime("%d/%m/%Y %H:%M")
                if tournament.ended_at is not None
                else "N/C",
                "time_control": tournament.time_control,
                "number_of_rounds": tournament.number_of_rounds,
                "number_of_players": len(tournament.players),
            },
        )

    def update(self, identifier: int):
        """
        Update tournament

        :param identifier:
        :return:
        """

        tournament: Tournament = self._entity_manager.get_repository(Tournament).find(identifier)

        if tournament.get_state() != "pending":
            Console.print("Vous ne pouvez pas modifier un tournois commencé.", Console.FAIL)

        def handler(tournament_: Tournament):
            self._entity_manager.update(tournament_)
            Console.print("Tournois modifié avec succès !", Console.SUCCESS)
            self.redirect("tournament_read", [identifier])

        form: TournamentForm = TournamentForm(handler, tournament)
        self._form(
            form,
            "tournament/update",
            {
                "identifier": tournament.identifier,
                "name": tournament.name,
                "state": tournament.state,
                "description": tournament.description,
                "location": tournament.location,
                "started_at": tournament.started_at.strftime("%d/%m/%Y %H:%M"),
                "ended_at": tournament.ended_at.strftime("%d/%m/%Y %H:%M")
                if tournament.ended_at is not None
                else "N/C",
                "time_control": tournament.time_control,
                "number_of_rounds": tournament.number_of_rounds,
                "number_of_players": len(tournament.players),
            },
        )

    def start(self, identifier: int):
        """
        Start tournament

        :param identifier:
        :return:
        """
        tournament: Tournament = self._entity_manager.get_repository(Tournament).find(identifier)

        if not self._workflow.can(tournament, "start"):
            Console.print("Vous ne pouvez pas démarrer ce tournois.", Console.FAIL)
            self.redirect("tournament_read", [identifier])

        self._workflow.apply(tournament, "start")

        self._entity_manager.update(tournament)
        Console.print("Tournois démarré avec succès !", Console.SUCCESS)
        self.redirect("tournament_read", [identifier])

    def ranking(self, identifier: int):
        """
        Tournament's ranking

        :param identifier:
        :return:
        """
        tournament: Tournament = self._entity_manager.get_repository(Tournament).find(identifier)

        tournament.generate_ranking()

        self._list(
            headers=[
                Header(1, "Rang", lambda player: str(player.rank)),
                Header(2, "Nom", lambda player: f"{player.first_name} {player.last_name}"),
                Header(3, "Points", lambda player: str(player.points)),
                Header(4, "Nombre de matchs", lambda player: str(len(player.opponents))),
            ],
            data=tournament.players,
            callback=lambda tournament: str(tournament.identifier),
            backward="tournament_read",
            backward_params=[identifier],
        )
