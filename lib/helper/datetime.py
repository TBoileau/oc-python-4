"""Imported modules/packages"""
from datetime import datetime


class Datetime(datetime):
    """
    Datetime class
    """

    @staticmethod
    def is_valid(string: str, format_: str) -> bool:
        """
        Check if datetime is valid
        :param string:
        :param format_:
        :return:
        """
        try:
            datetime.strptime(string, format_)
            return True
        except ValueError:
            return False
