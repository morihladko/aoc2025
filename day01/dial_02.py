from operator import ne
import sys


def count_rotations(start_position: int, lines: list[str]) -> int:
    position = start_position
    rotations = 0

    for line in lines:
        direction = line[0]
        amount = int(line[1:])

        if amount == 0:
            continue

        if direction == "R":
            next_position = position + amount
            rotations += next_position // 100
        elif direction == "L":
            next_position = position - amount
            rotations += ((position -1) // 100) - ((next_position -1) // 100)
        else:
            raise ValueError(f"Invalid direction: {direction}")

        position = next_position % 100

    return rotations


def parse_input() -> list[str]:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            lines = file.readlines()
    else:
        lines = sys.stdin.readlines()

    return [line.strip() for line in lines]


def main() -> None:
    lines = parse_input()
    start_position = 50
    result = count_rotations(start_position, lines)
    print(result)


if __name__ == "__main__":
    main()
