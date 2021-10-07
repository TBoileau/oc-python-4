"""Imported modules/packages"""
import re
import uuid
from datetime import datetime
from re import Pattern
from typing import Dict, Any

from src.entity.tournament import Tournament
from src.form.form import Form
from src.helper.datetime import Datetime
from src.input.input import Input


class TournamentForm(Form):
    """
    Tournament form
    """

    def _transform(self, values: Dict[str, Any], data: Any = None) -> Tournament:
        return Tournament(
            identifier=uuid.uuid4(),
            name=values["name"],
            description=values["description"],
            location=values["location"],
            started_at=values["started_at"],
            ended_at=values["ended_at"],
            number_of_rounds=values["number_of_rounds"],
            time_control=values["time_control"],
        )

    def _build(self, inputs: Dict[str, Input]):
        date_pattern: Pattern = re.compile(r"^\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}$")
        time_controls: Dict[int, str] = {
            0: Tournament.TYPE_BULLET,
            1: Tournament.TYPE_SPEED,
            2: Tournament.TYPE_BLITZ,
        }
        inputs["name"] = Input(
            label="Nom du tournois : ",
            message="Ce champ ne peut pas être vide.",
            validate=lambda raw_data: raw_data.strip() != "",
        )
        inputs["description"] = Input(
            label="Description du tournois : ",
            message="Ce champ ne peut pas être vide.",
            validate=lambda raw_data: raw_data.strip() != "",
        )
        inputs["location"] = Input(
            label="Localisation : ",
            message="Ce champ ne peut pas être vide.",
            validate=lambda raw_data: raw_data.strip() != "",
        )
        inputs["time_control"] = Input(
            label="Type (0: Bullet, 1: Speed, 2: Blitz) : ",
            message="Veuillez saisir un chiffre entre 0 et 2.",
            validate=lambda raw_data: re.match(r"^\d+$", raw_data) and int(raw_data) in [0, 1, 2],
            transform=lambda raw_data: time_controls[int(raw_data)],
        )
        inputs["number_of_rounds"] = Input(
            label="Nombre de rondes : ",
            message="Veuillez saisir un chiffre supérieur à 0.",
            validate=lambda raw_data: re.match(r"^\d+$", raw_data) and int(raw_data) > 0,
            transform=int,
        )
        inputs["started_at"] = Input(
            label="Date de début (JJ/MM/AAAA HH:MM) : ",
            message="Veuillez saisir un date et heure au format suivant : JJ/MM/AAAA HH:MM.",
            validate=lambda raw_data: raw_data.strip() != ""
            and date_pattern.match(raw_data) is not None
            and Datetime.is_valid(raw_data, "%d/%m/%Y %H:%M"),
            transform=lambda raw_data: datetime.strptime(raw_data, "%d/%m/%Y %H:%M"),
        )
        inputs["ended_at"] = Input(
            label="Date de fin (JJ/MM/AAAA HH:MM) : ",
            message="Veuillez saisir un date et heure au format suivant : JJ/MM/AAAA HH:MM.",
            validate=lambda raw_data: raw_data.strip() == ""
            or date_pattern.match(raw_data) is not None
            and Datetime.is_valid(raw_data, "%d/%m/%Y %H:%M"),
            transform=lambda raw_data: datetime.strptime(raw_data, "%d/%m/%Y %H:%M"),
        )
