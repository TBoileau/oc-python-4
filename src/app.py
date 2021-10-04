"""Imported modules/packages"""


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

        return self.__launched
