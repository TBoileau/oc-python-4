"""Imported modules/packages"""
from typing import List, Callable, Any

from src.controller.abstract_controller import AbstractController
from src.entity.player import Player
from src.entity.tournament import Tournament
from src.form.tournament_form import TournamentForm
from src.gateway.player_gateway import PlayerGateway
from src.gateway.tournament_gateway import TournamentGateway
from src.helper.console import Console
from src.input.input import Input
from src.representation.header import Header
from src.representation.representation import Representation
from src.representation.representation_factory_interface import RepresentationFactoryInterface
from src.router.router_interface import RouterInterface
from src.templating.templating_interface import TemplatingInterface
from src.workflow.workflow_interface import WorkflowInterface


class TournamentController(AbstractController):
    """
    App controller
    """

    def __init__(
        self,
        templating: TemplatingInterface,
        router: RouterInterface,
        tournament_gateway: TournamentGateway,
        player_gateway: PlayerGateway,
        representation_factory: RepresentationFactoryInterface,
        workflow: WorkflowInterface,
    ):
        super().__init__(templating, router)
        self.__tournament_gateway: TournamentGateway = tournament_gateway
        self.__player_gateway: PlayerGateway = player_gateway
        self.__representation_factory: RepresentationFactoryInterface = representation_factory
        self.__workflow: WorkflowInterface = workflow

    def create(self):
        """
        Create tournament

        :return:
        """

        def handler(tournament: Tournament):
            self.__tournament_gateway.persist(tournament)
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
        tournament: Tournament = self.__tournament_gateway.find(identifier)

        if tournament.get_state() != "pending":
            Console.print("Vous ne pouvez pas inscrire un joueur alors dans un tournois commencé.", Console.FAIL)

        player: Player = self.__player_gateway.find(player_id)

        tournament.players.remove(player)

        self.__tournament_gateway.update(tournament)

        Console.print("Joueur désinscrit avec succès.", Console.SUCCESS)

        self.redirect("tournament_players", [identifier])

    def register(self, identifier: int, player_id: int):
        """
        Register player from tournament
        :param identifier:
        :param player_id:
        :return:
        """
        tournament: Tournament = self.__tournament_gateway.find(identifier)

        player: Player = self.__player_gateway.find(player_id)

        tournament.players.append(player)

        self.__tournament_gateway.update(tournament)

        Console.print("Joueur inscrit avec succès.", Console.SUCCESS)

        self.redirect("tournament_registration", [identifier])

    def players(self, identifier: int):
        """
        List tournaments players
        :param identifier:
        :return:
        """
        tournament: Tournament = self.__tournament_gateway.find(identifier)

        representation: Representation = self.__representation_factory.create()
        representation.add_header(Header(1, "Identifiant", lambda player: str(player.identifier)))
        representation.add_header(Header(2, "Nom", lambda player: f"{player.first_name} {player.last_name}"))
        representation.set_data(tournament.players)
        representation.render()

        identifiers: List[Any] = list(map(lambda player: str(player.identifier), tournament.players))

        input_: Input = Input(
            label="Saisissez l'identifiant d'un joueur que vous souhaitez désinscrire"
            ", I pour inscrire un joueur ou R pour retour : ",
            message="Veuillez saisir 'A', 'R', 'I ou un identifiant parmi la liste.",
            transform=str,
            validate=lambda raw_data: raw_data in ["R", "A", "I"] + identifiers,
        )

        def redirect_to_tournament(player_id: int) -> Callable:
            return lambda: self.redirect("tournament_unregister", [identifier, int(player_id)])

        self._choice(
            input_,
            {
                **{
                    "R": lambda: self.redirect("tournament_read", [identifier]),
                    "I": lambda: self.redirect("tournament_registration", [identifier]),
                },
                **dict(zip(identifiers, map(redirect_to_tournament, identifiers))),
            },
        )

    def registration(self, identifier: int):
        """
        Registration player in tournament
        :param identifier:
        :return:
        """
        tournament: Tournament = self.__tournament_gateway.find(identifier)

        if tournament.get_state() != "pending":
            Console.print("Vous ne pouvez pas inscrire un joueur alors dans un tournois commencé.", Console.FAIL)

        players: List[Player] = [
            player for player in self.__player_gateway.find_all() if player not in tournament.players
        ]

        representation: Representation = self.__representation_factory.create()
        representation.add_header(Header(1, "Identifiant", lambda player: str(player.identifier)))
        representation.add_header(Header(2, "Nom", lambda player: f"{player.first_name} {player.last_name}"))
        representation.set_data(players)
        representation.render()

        identifiers: List[Any] = list(map(lambda player: str(player.identifier), players))

        input_: Input = Input(
            label="Saisissez l'identifiant d'un joueur que vous souhaitez inscrire ou R pour retour : ",
            message="Veuillez saisir 'R' ou un identifiant parmi la liste.",
            transform=str,
            validate=lambda raw_data: raw_data in ["R"] + identifiers,
        )

        def redirect_to_tournament(player_id: int) -> Callable:
            return lambda: self.redirect("tournament_register", [identifier, int(player_id)])

        self._choice(
            input_,
            {
                **{
                    "R": lambda: self.redirect("tournament_players", [identifier]),
                },
                **dict(zip(identifiers, map(redirect_to_tournament, identifiers))),
            },
        )

    def list(self):
        """
        List tournaments

        :return:
        """
        tournaments: List[Tournament] = self.__tournament_gateway.find_all()

        representation: Representation = self.__representation_factory.create()
        representation.add_header(Header(1, "Identifiant", lambda tournament: str(tournament.identifier)))
        representation.add_header(Header(2, "Nom", lambda tournament: tournament.name))
        representation.add_header(Header(3, "Statut", lambda tournament: tournament.state))
        representation.set_data(tournaments)
        representation.render()

        identifiers: List[int] = list(map(lambda tournament: tournament.identifier, tournaments))

        input_: Input = Input(
            label="Saisissez l'identifiant du tournois que vous souhaitez sélectionner (0 pour quitter) : ",
            message="Veuillez saisir 0 ou un identifiant parmi la liste.",
            transform=int,
            validate=lambda raw_data: raw_data.isnumeric() and int(raw_data) in [0] + identifiers,
        )

        def redirect_to_tournament(identifier: int) -> Callable:
            return lambda: self.redirect("tournament_read", [identifier])

        self._choice(
            input_,
            {
                **{0: lambda: self.redirect("app_home")},
                **dict(zip(identifiers, map(redirect_to_tournament, identifiers))),
            },
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

        tournament: Tournament = self.__tournament_gateway.find(identifier)

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

        tournament: Tournament = self.__tournament_gateway.find(identifier)

        if tournament.get_state() != "pending":
            Console.print("Vous ne pouvez pas modifier un tournois commencé.", Console.FAIL)

        def handler(tournament_: Tournament):
            self.__tournament_gateway.update(tournament_)
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
        tournament: Tournament = self.__tournament_gateway.find(identifier)

        if not self.__workflow.can(tournament, "start"):
            Console.print("Vous ne pouvez pas démarrer ce tournois.", Console.FAIL)
            self.redirect("tournament_read", [identifier])

        self.__workflow.apply(tournament, "start")

        self.__tournament_gateway.update(tournament)
        Console.print("Tournois démarré avec succès !", Console.SUCCESS)
        self.redirect("tournament_read", [identifier])

    def ranking(self, identifier: int):
        """
        Tournament's ranking

        :param identifier:
        :return:
        """
        tournament: Tournament = self.__tournament_gateway.find(identifier)

        tournament.generate_ranking()

        representation: Representation = self.__representation_factory.create()
        representation.add_header(Header(1, "Rang", lambda player: str(player.rank)))
        representation.add_header(Header(2, "Nom", lambda player: f"{player.first_name} {player.last_name}"))
        representation.add_header(Header(3, "Points", lambda player: str(player.points)))
        representation.add_header(Header(4, "Nombre de matchs", lambda player: str(len(player.opponents))))
        representation.set_data(tournament.players)
        representation.render()

        input_: Input = Input(
            label="Saisissez R pour retour : ",
            message="Veuillez saisir R.",
        )

        self._choice(
            input_,
            {
                "R": lambda: self.redirect("tournament_read", [identifier]),
            },
        )
