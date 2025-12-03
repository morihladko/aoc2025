import sys

type BatteryBank = list[int]
type Battery = list[BatteryBank]


def max_with_index(values: list[int]) -> tuple[int, int]:
    try:
        max_value = values[0]
        max_index = 0

        for index, value in enumerate(values[1:], start=1):
            if value > max_value:
                max_value = value
                max_index = index

        return max_value, max_index
    except IndexError as e:
        raise ValueError("Cannot find max of empty list") from e


def find_max_joltage(battery_bank: BatteryBank) -> int:
    max_joultage = 0

    for digit_i in range(0, 12):
        digits_left = 12 - digit_i - 1
        max_digit, max_digit_index = max_with_index(
            battery_bank[: (-digits_left if digits_left > 0 else None)]
        )
        max_joultage += max_digit * (10**digits_left)
        battery_bank = battery_bank[max_digit_index + 1 :]

    return max_joultage


def count_joltage(battery: Battery) -> int:
    return sum(find_max_joltage(battery_bank) for battery_bank in battery)


def parse_input() -> Battery:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            lines = file.readlines()
    else:
        lines = sys.stdin.readlines()

    return [[int(digit) for digit in line.strip()] for line in lines]


def main() -> None:
    lines = parse_input()
    result = count_joltage(lines)
    print(result)


if __name__ == "__main__":
    main()
