import sys


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not ranges:
        return []

    # Sort ranges by their start value
    ranges.sort(key=lambda r: r[0])

    merged = []
    current_start, current_end = ranges[0]

    for start, end in ranges[1:]:
        if start <= current_end:  # Overlapping or contiguous ranges
            current_end = max(current_end, end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = start, end

    # Append the last range
    merged.append((current_start, current_end))

    return merged

def count_fresh_ingredients(ranges: list[tuple[int, int]], ingredients: list[int]) -> int:
    ranges = merge_ranges(ranges)
    ingredients = sorted(ingredients)

    fresh_count = 0
    for ingredient in ingredients:
        is_fresh = False
        for start, end in ranges:
            if start <= ingredient <= end:
                is_fresh = True
                break
        if is_fresh:
            fresh_count += 1

    return fresh_count


def parse_input() -> tuple[list[tuple[int, int]], list[int]]:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            lines = file.readlines()
    else:
        lines = sys.stdin.readlines()
    
    lines_iterator = iter(lines)
    fresh_ranges = []
    while line := next(lines_iterator).strip():
        if line == "":
            break
        fresh_ranges.append(tuple(map(int, line.split("-"))))  # type: ignore

    ingredients = [int(line.strip()) for line in lines_iterator]

    return fresh_ranges, ingredients


def main() -> None:
    fresh_ranges, ingredients  = parse_input()
    result = count_fresh_ingredients(fresh_ranges, ingredients)
    print(result)


if __name__ == "__main__":
    main()
