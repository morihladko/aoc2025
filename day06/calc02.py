from itertools import groupby
import sys
from functools import reduce
from typing import Literal

type Operator = Literal["+", "*"]


def transpone(lines: list[str]) -> list[str]:
    """
    >>> transpone(['123 328  51 64 ', ' 45 64  387 23 ', '  6 98  215 314'])
    ['  4', '431', '623', '   ', '175', '581', ' 32', '   ', '8  ', '248', '369', '   ', '356', '24 ', '1  ']
    """

    if not lines:
        return []

    return ["".join(row) for row in reversed(list(zip(*lines)))]


def compute_grand_total(
    number_groups: list[list[int]], operators: list[Operator]
) -> int:
    grand_total = 0
    for i, group in enumerate(number_groups):
        operator = operators[i]
        if operator == "+":
            grand_total += sum(group)
        elif operator == "*":
            grand_total += reduce(lambda x, y: x * y, group, 1)

    return grand_total


def parse_number_groups(raw_lines: list[str]) -> list[list[int]]:
    """
    >>> from itertools import groupby
    >>> parse_number_groups(['123 ', ' 28', '  1', '   ', '145', '6  ', '27 '])
    [[123, 28, 1], [145, 6, 27]]
    """
    return [
        [int(line) for line in group]
        for is_number, group in groupby(raw_lines, key=lambda x: bool(x.strip()))
        if is_number
    ]


def parse_input() -> tuple[list[list[int]], list[Operator]]:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            lines = file.readlines()
    else:
        lines = sys.stdin.readlines()

    transposed_lines = transpone([line[:-1] for line in lines[:-1]])
    operators: list[Operator] = list(reversed(lines[-1].split()))  # type: ignore

    return parse_number_groups(transposed_lines), operators


def main() -> None:
    number_groups, operators = parse_input()
    result = compute_grand_total(number_groups, operators)
    print(result)


if __name__ == "__main__":
    main()
