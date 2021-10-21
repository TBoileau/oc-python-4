"""Imported modules/packages"""


class Console:
    """
    Console class
    """

    SUCCESS: str = "\033[92m"
    WARNING = "\033[93m"
    FAIL: str = "\033[91m"
    END: str = "\033[0m"
    BOLD: str = "\033[1m"
    UNDERLINE: str = "\033[4m"

    @staticmethod
    def print(text: str, style: str):
        """
        Print styled text

        :param text:
        :param style:
        :return:
        """
        print(f"{style}{text}{Console.END}")

    @staticmethod
    def input(text: str, style: str) -> str:
        """
        Add styled input

        :param text:
        :param style:
        :return:
        """
        return input(f"{style}{text}{Console.END}")
