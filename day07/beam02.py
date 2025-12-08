import sys


def bump_dynamic_map_count(line: list[str | int], index: int, count: int) -> None:
    if index < 0 or index >= len(line):
        return

    if type(line[index]) is int:  # pylint: disable=unidiomatic-typecheck
        line[index] += count  # type: ignore
    else:
        line[index] = count


def count_beam_splits(map_: list[str]) -> int:
    dynamic_map: list[list[str | int]] = [list(line) for line in map_]
    prev_line = [1 if c == "S" else c for c in dynamic_map[0]]

    for line in dynamic_map[1:]:
        for i, character in enumerate(line):
            if type(prev_line[i]) is int:  # pylint: disable=unidiomatic-typecheck
                count: int = prev_line[i]  # type: ignore
                if character == "^":
                    bump_dynamic_map_count(line, i - 1, count)
                    bump_dynamic_map_count(line, i + 1, count)
                else:
                    bump_dynamic_map_count(line, i, count)
        prev_line = line

    return sum(c for c in prev_line if type(c) is int)  # type: ignore, pylint: disable=unidiomatic-typecheck


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
