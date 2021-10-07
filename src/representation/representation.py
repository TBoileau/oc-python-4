"""Imported modules/packages"""
from typing import Dict, Any, List, Tuple

from src.helper.string import String
from src.representation.header import Header
from src.representation.representation_interface import RepresentationInterface


class Representation(RepresentationInterface):
    """
    Representation class
    """

    __headers: Dict[int, Header] = {}
    __data: List[Dict[int, str]] = []

    def add_header(self, header: Header):
        self.__headers[header.order] = header

    def set_data(self, data: List[Any]):
        assert len(self.__headers) > 0

        for row in data:
            row_data: Dict[int, str] = {}
            for header in self.__headers.values():
                row_data[header.order] = header.callback(row)
                header.length = max(len(row_data[header.order]), header.length)
            self.__data.append(row_data)

    def render(self):
        assert len(self.__headers) > 0

        self.__print_line([(header.label, header.order) for header in self.__headers.values()])

        if len(self.__data) == 0:
            self.__print_line([("", index) for index in self.__headers])
        else:
            for row in self.__data:
                self.__print_line([(column, index) for index, column in row.items()])

        print("")

    def __print_line(self, columns: List[Tuple[str, int]], first: bool = False):
        line: str = "|".join(
            list(map(lambda column: String.bfill(column[0], " ", self.__headers[column[1]].length + 6), columns))
        )
        if first:
            print(f"▕{''.join(['-' for i in range(len(line))])}▏")
        print(f"▕{line}▏")
        print(f"▕{''.join(['-' for i in range(len(line))])}▏")
