import sys


def count_zero_positions(start_position: int, lines: list[str]) -> int:
    position = start_position
    zero_positions = 0

    for line in lines:
        direction = line[0]
        amount = int(line[1:])

        if direction == "R":
            next_position = position + amount
        elif direction == "L":
            next_position = position + (100 - amount)
        else:
            raise ValueError(f"Invalid direction: {direction}")

        position = next_position % 100
        zero_positions += position == 0

    return zero_positions


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
    result = count_zero_positions(start_position, lines)
    print(result)


if __name__ == "__main__":
    main()
