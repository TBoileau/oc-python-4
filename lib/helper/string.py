"""Imported modules/packages"""


class String:
    """
    String helper
    """

    @staticmethod
    def bfill(text: str, character: str, max_length: int) -> str:
        """
        Fill character before and after text

        :param text:
        :param character:
        :param max_length:
        :return:
        """
        if len(text) == max_length:
            return text

        start: int = (max_length - len(text)) // 2
        end: int = (max_length - len(text)) - start

        prefix: str = "".join([character for i in range(1, start)]) if start > 0 else ""
        suffix: str = "".join([character for i in range(1, end)] if end > 0 else "")

        return f"{prefix}{text}{suffix}"
