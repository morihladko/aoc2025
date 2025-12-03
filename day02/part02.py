from functools import lru_cache
import sys
from typing import Generator


def divisors_generator(n: int) -> Generator[int, None, None]:
    for i in range(1, n // 2 + 1):
        if n % i == 0:
            yield i


@lru_cache(maxsize=1_000_000)
def count_digits(n: int) -> int:
    count = 0

    if n == 0:
        return 1

    n = abs(n)
    while n > 0:
        n //= 10
        count += 1

    return count


def split_to_chunks(n: int, chunk_size: int) -> Generator[int, None, None]:
    divisor = 10**chunk_size

    n = abs(n)
    while n > 0:
        yield n % divisor

        n //= divisor


def invalid_ids(lower_bound: int, upper_bound: int) -> Generator[int, None, None]:
    for id_ in range(lower_bound, upper_bound + 1):
        digits_count = count_digits(id_)

        for chunk_size in divisors_generator(digits_count):
            chunks = split_to_chunks(id_, chunk_size)
            iter_chunks = iter(chunks)
            first = next(iter_chunks)

            if all(chunk == first for chunk in iter_chunks):
                yield id_
                break


def count_invalid_ids(ranges: list[tuple[int, int]]) -> int:
    sum_ = 0

    for lower_bound, upper_bound in ranges:
        for invalid_id in invalid_ids(lower_bound, upper_bound):
            sum_ += invalid_id

    return sum_


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
