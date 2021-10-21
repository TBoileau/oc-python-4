"""Imported modules/packages"""
from typing import Dict, Any, List, Tuple, Callable

from lib.helper.string import String
from lib.representation.header import Header
from lib.representation.representation_interface import RepresentationInterface


class Representation(RepresentationInterface):
    """
    Representation class
    """

    def __init__(self, callback: Callable):
        self.__headers: Dict[int, Header] = {}
        self.__data: List[Dict[int, str]] = []
        self.__raw_data: List[Any] = []
        self.__identifiers: List[str] = []
        self.__callback: Callable = callback

    def add_header(self, header: Header):
        self.__headers[header.order] = header

    @property
    def identifiers(self) -> List[str]:
        return list(map(self.__callback, self.__raw_data))

    def set_data(self, data: List[Any]):
        assert len(self.__headers) > 0

        self.__raw_data = data

        for row in data:
            row_data: Dict[int, str] = {}
            for header in self.__headers.values():
                row_data[header.order] = header.callback(row)
                header.length = max(len(row_data[header.order]), header.length)
            self.__data.append(row_data)

    def render(self):
        assert len(self.__headers) > 0

        self.__print_line([(header.label, header.order) for header in self.__headers.values()], True)

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
