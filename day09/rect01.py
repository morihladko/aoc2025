import sys
from itertools import combinations

type Point2d = tuple[int, int]


def calculate_max_rectangle_area(rectangles: list[Point2d]) -> int:
    """
    >>> calculate_max_rectangle_area([(2, 3), (4, 5), (1, 10)])
    1
    """
    return max(
        (rect2[0] - rect1[0] - 1) * (rect2[1] - rect1[1] - 1)
        for rect1, rect2 in combinations(rectangles, 2)
    )


def print_map(rectangles: list[Point2d]) -> None:
    max_x = max(x for x, _ in rectangles)
    max_y = max(y for _, y in rectangles)

    grid = [["." for _ in range(max_x + 3)] for _ in range(max_y + 2)]

    for x, y in rectangles:
        grid[y][x] = "#"

    for row in grid:
        print("".join(row))


def parse_input() -> list[Point2d]:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            lines = file.readlines()
    else:
        lines = sys.stdin.readlines()

    return [tuple(map(int, line.strip().split(","))) for line in lines]  # type: ignore


def main() -> None:
    rectangles = parse_input()
    print_map(rectangles)
    max_rect_area = calculate_max_rectangle_area(rectangles)
    print(max_rect_area)


if __name__ == "__main__":
    main()
