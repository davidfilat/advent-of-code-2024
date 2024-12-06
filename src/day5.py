from typing import Any

from cytoolz import groupby, first, second, valmap, compose, curry, juxt, complement
from cytoolz.curried import map, get, filter
from cytoolz.functoolz import pipe

from utils.common import get_day_input, print_result
from utils.functools import apply
from utils.itertools import intersection, swap_elements

T_RULES = dict[int, list[int]]
T_UPDATE = list[int]


def parse_rules(rules: str) -> T_RULES:
    unpacked_rules = map(
        lambda rule: [int(x) for x in rule.strip().split("|")], rules.split("\n")
    )
    return valmap(compose(list, map(second)), groupby(first, unpacked_rules))


def parse_updates(updates: str) -> list[T_UPDATE]:
    return [[int(x) for x in line.strip().split(",")] for line in updates.split("\n")]


def parse_input(text: str) -> tuple[T_RULES, list[T_UPDATE]]:
    rules, updates = [x.strip() for x in text.split("\n\n")]
    return parse_rules(rules), parse_updates(updates)


@curry
def find_rule_breaker(rules: T_RULES, update: T_UPDATE) -> tuple[Any, Any] | None:
    for i in pipe(update, len, range):
        x = get(i, update)
        must_be_before = get(x, rules, [])
        if broken_rules := intersection(must_be_before, update[:i]):
            return i, pipe(broken_rules, first, update.index)
    return None


def get_middle_element(seq: list[int]) -> int:
    return get(len(seq) // 2, seq)


@curry
def is_valid_update(rules: T_RULES, update: T_UPDATE) -> bool:
    return find_rule_breaker(rules, update) is None


@curry
def fix_update(rules: T_RULES, update: T_UPDATE) -> list[int]:
    broken_rule = find_rule_breaker(rules, update)
    return (
        update
        if broken_rule is None
        else fix_update(rules, swap_elements(update, *broken_rule))
    )


part_1 = compose(
    sum,
    map(get_middle_element),
    apply(filter),
    juxt(compose(is_valid_update, first), second),
    parse_input,
)


def part_2(text: str) -> int:
    rules, updates = parse_input(text)

    return pipe(
        updates,
        filter(complement(is_valid_update(rules))),
        map(fix_update(rules)),
        map(get_middle_element),
        sum,
    )


if __name__ == "__main__":
    text = get_day_input(5)
    print_result(1, part_1(text))
    print_result(2, part_2(text))
