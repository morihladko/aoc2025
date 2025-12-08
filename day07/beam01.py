import sys


def count_beam_splits(map_: list[str]) -> int:
    start_line = map_[0]
    beam_positions = {start_line.find("S")}
    split_count = 0

    for line in map_[1:]:
        new_beam_positions = set()
        for position in beam_positions:
            if line[position] == "^":
                split_count += 1
                left_pos = position - 1
                right_pos = position + 1

                if left_pos >= 0:
                    new_beam_positions.add(left_pos)
                if right_pos < len(line):
                    new_beam_positions.add(right_pos)
            else:
                new_beam_positions.add(position)
        beam_positions = new_beam_positions

    return split_count


def parse_input() -> list[str]:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            lines = file.readlines()
    else:
        lines = sys.stdin.readlines()

    return [line.strip() for line in lines]


def main() -> None:
    map_ = parse_input()
    result = count_beam_splits(map_)
    print(result)


if __name__ == "__main__":
    main()
