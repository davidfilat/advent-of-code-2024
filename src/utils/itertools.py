from cytoolz import curry, drop, take


@curry
def drop_nth(n: int, iterable: list) -> list:
    return [*take(n, iterable), *drop(n + 1, iterable)]
