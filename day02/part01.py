import sys
from typing import Generator


def count_digits(n: int) -> int:
    count = 0

    if n == 0:
        return 1

    n = abs(n)

    while n > 0:
        n //= 10
        count += 1

    return count


def invalid_ids(lower_bound: int, upper_bound: int) -> Generator[int, None, None]:
    for id_ in range(lower_bound, upper_bound + 1):
        digits_count = count_digits(id_)

        if digits_count % 1:
            continue
        
        left_number = id_ // (10 ** (digits_count // 2))
        right_number = id_ % (10 ** (digits_count // 2))

        if left_number == right_number:
            yield id_



def count_invalid_ids(ranges: list[tuple[int, int]]) -> int:
    return sum(
        id_
        for lower_bound, upper_bound in ranges
        for id_ in invalid_ids(lower_bound, upper_bound)
    )


def parse_input() -> list[tuple[int, int]]:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            data = file.readline().strip()
    else:
        data = sys.stdin.readline().strip()

    result = []
    for id_ranges in data.split(","):
        id_range = tuple(map(int, id_ranges.split("-")))
        if len(id_range) == 2:
            result.append((id_range[0], id_range[1]))
        else:
            raise ValueError(f"Invalid range format: {id_ranges}")
    return result


def main():
    data = parse_input()

    sum_of_invalid_ranges = count_invalid_ids(data)

    print(sum_of_invalid_ranges)


if __name__ == "__main__":
    main()
