import sys
from functools import reduce
from typing import Literal

type Operator = Literal["+", "*"]


def transpone(matrix: list[list[int]]) -> list[list[int]]:
    if not matrix:
        return []
    return [list(row) for row in zip(*matrix)]


def compute_grand_total(columns: list[list[int]], operators: list[Operator]) -> int:
    rows = transpone(columns)

    grand_total = 0
    for operator in operators:
        if operator == "+":
            grand_total += sum(rows.pop(0))
        elif operator == "*":
            grand_total += reduce(lambda x, y: x * y, rows.pop(0), 1)

    return grand_total


def parse_input() -> tuple[list[list[int]], list[Operator]]:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            lines = file.readlines()
    else:
        lines = sys.stdin.readlines()

    columns = [[int(value) for value in line.strip().split()] for line in lines[:-1]]
    operators: list[Operator] = lines[-1].strip().split()  # type: ignore

    return columns, operators


def main() -> None:
    columns, operators = parse_input()
    result = compute_grand_total(columns, operators)
    print(result)


if __name__ == "__main__":
    main()
