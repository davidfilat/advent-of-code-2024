from typing import TypeVar

from cytoolz import curry, drop, take

T = TypeVar("T")


@curry
def drop_nth(n: int, iterable: list[T]) -> list[T]:
    return [*take(n, iterable), *drop(n + 1, iterable)]


def intersection(list1: list[T], list2: list[T]) -> list[T]:
    """Finds the intersection of two lists."""
    return list(set(list1) & set(list2))
