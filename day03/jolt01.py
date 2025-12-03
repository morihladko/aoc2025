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
    first_digit, first_index = max_with_index(battery_bank[:-1])
    battery_bank = battery_bank[first_index + 1 :]
    second_digit, _ = max_with_index(battery_bank)

    return first_digit * 10 + second_digit


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
