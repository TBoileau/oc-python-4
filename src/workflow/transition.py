"""Imported modules/packages"""
from typing import List, Callable, Optional


class Transition:
    """
    Transition
    """

    def __init__(
        self,
        name: str,
        from_states: List[str],
        to_state: str,
        guard: Optional[Callable] = None,
        completed: Optional[Callable] = None,
    ):
        self.name: str = name
        self.from_states: List[str] = from_states
        self.to_state: str = to_state
        self.guard: Callable = guard
        self.completed: Callable = completed
