from typing import Callable, TypeVar, Tuple, Any

from typing import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


def apply(func: Callable[P, R]) -> Callable[[Tuple[Any, ...]], R]:
    return lambda args: func(*args)
