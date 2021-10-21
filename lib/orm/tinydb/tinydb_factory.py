"""Imported modules/packages"""
from tinydb import TinyDB


class TinyDBFactory:
    """
    TinyDB factory
    """

    @staticmethod
    def create(url: str) -> TinyDB:
        """
        Create an instance of TinyDB

        :param url:
        :return:
        """
        return TinyDB(url)
