"""Imported modules/packages"""
from dotenv import load_dotenv


class App:
    """
    App class
    """

    __launched: bool = False

    def run(self) -> bool:
        """
        Run app

        :return:
        """
        self.__launched = True
        load_dotenv()
        return self.__launched
