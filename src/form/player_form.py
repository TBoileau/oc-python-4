"""Imported modules/packages"""
import re
from datetime import datetime
from re import Pattern
from typing import Dict, Any, Optional

from src.entity.player import Player
from src.form.form import Form
from src.helper.datetime import Datetime
from src.input.input import Input


class PlayerForm(Form):
    """
    Tournament form
    """

    def _transform(self, values: Dict[str, Any], data: Optional[Player] = None) -> Player:
        if data is None:
            return Player(
                first_name=values["first_name"],
                last_name=values["last_name"],
                birthday=values["birthday"],
                gender=values["gender"],
                ranking=values["ranking"],
            )

        data.first_name = values["first_name"]
        data.last_name = values["last_name"]
        data.birthday = values["birthday"]
        data.gender = values["gender"]
        data.ranking = values["ranking"]
        return data

    def _build(self, inputs: Dict[str, Input]):
        date_pattern: Pattern = re.compile(r"^\d{2}\/\d{2}\/\d{4}$")
        genders: Dict[str, str] = {
            "H": Player.GENDER_MALE,
            "F": Player.GENDER_FEMALE,
            "NB": Player.GENDER_NON_BINARY,
        }
        inputs["first_name"] = Input(
            label="Prénom : ",
            message="Ce champ ne peut pas être vide.",
            validate=lambda raw_data: raw_data.strip() != "",
        )
        inputs["last_name"] = Input(
            label="Nom : ",
            message="Ce champ ne peut pas être vide.",
            validate=lambda raw_data: raw_data.strip() != "",
        )
        inputs["gender"] = Input(
            label="Sexe (H: Homme, F: Femme, NB: Non binaire) : ",
            message="Veuillez saisir un chiffre entre 0 et 2.",
            validate=lambda raw_data: raw_data in ["H", "F", "NB"],
            transform=lambda raw_data: genders[raw_data],
        )
        inputs["birthday"] = Input(
            label="Date de naissance (JJ/MM/AAAA) : ",
            message="Veuillez saisir un date au format suivant : JJ/MM/AAAA.",
            validate=lambda raw_data: raw_data.strip() != ""
            and date_pattern.match(raw_data) is not None
            and Datetime.is_valid(raw_data, "%d/%m/%Y"),
            transform=lambda raw_data: datetime.strptime(raw_data, "%d/%m/%Y").date(),
        )
        inputs["ranking"] = Input(
            label="Classement : ",
            message="Veuillez saisir un nombre.",
            validate=lambda raw_data: raw_data.isnumeric(),
            transform=int,
        )
