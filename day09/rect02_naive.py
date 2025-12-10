import math
import re
import sys
from itertools import combinations

type Point2d = tuple[int, int]


def rectangle_edge_tiles(a: Point2d, b: Point2d) -> list[Point2d]:
    """
    >>> rectangle_edge_tiles((1, 1), (3, 1))
    [(1, 1), (2, 1), (3, 1)]
    >>> rectangle_edge_tiles((1, 1), (1, 3))
    [(1, 1), (1, 2), (1, 3)]
    >>> rectangle_edge_tiles((1, 1), (3, 3))
    [(1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (1, 3), (2, 3), (3, 3)]
    """
    x1, y1 = a
    x2, y2 = b

    min_x = min(x1, x2)
    max_x = max(x1, x2)
    min_y = min(y1, y2)
    max_y = max(y1, y2)

    edge_tiles: list[Point2d] = []

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if x == min_x or x == max_x or y == min_y or y == max_y:
                edge_tiles.append((x, y))

    return edge_tiles

def calculate_max_rectangle_area(rectangles: list[Point2d]) -> int:
    rect_combinations = combinations(rectangles, 2)
    size_of_rect_combinations = math.comb(len(rectangles), 2)
    inside_rects: list[tuple[Point2d, Point2d]] = []

    for i, rect in enumerate(rect_combinations):
        # use ncurses to print status of current iteration
        print(f"Processing item {i + 1} of {size_of_rect_combinations}...", end='\r', flush=True)

        rect_boundary = rectangle_edge_tiles(rect[0], rect[1])
        for point in rect_boundary:
            if point_in_polygon_grid(point, rectangles) == -1:
                break
        else:
            inside_rects.append(rect)
    print()  # newline after progress output

    return max(
        math.prod((rect2[0] - rect1[0] - 1, rect2[1] - rect1[1] - 1))
        for rect1, rect2 in inside_rects
    )


def point_in_polygon_grid(point: Point2d, poly: list[Point2d]) -> int:
    """
    Pure integer point-in-polygon for axis-aligned polygons.

    Returns:
      1 -> inside
      0 -> on edge
     -1 -> outside

    (px, py) is an integer grid point (your "tile").
    """
    px, py = point
    crossings = 0
    n = len(poly)

    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]

        if x1 == x2:
            # vertical edge
            # on-edge check
            if px == x1 and min(y1, y2) <= py <= max(y1, y2):
                return 0

            # ray to the right: count intersection if edge is to the right
            # and spans py in a half-open interval
            if px < x1 and ((y1 <= py < y2) or (y2 <= py < y1)):
                crossings += 1

        elif y1 == y2:
            # horizontal edge: only on-edge matters
            if py == y1 and min(x1, x2) <= px <= max(x1, x2):
                return 0

    return 1 if (crossings % 2) == 1 else -1


def print_filled_polygon(poly: list[Point2d], offset: int = 1) -> None:
    """
    Print a filled polygon using '.' (empty) and '#' (filled),
    treating each integer (x, y) as one tile.

    The printed area goes from:
      x = 0 .. max_x + offset
      y = 0 .. max_y + offset
    """
    max_x = max(x for x, _ in poly)
    max_y = max(y for _, y in poly)

    width = max_x + offset + 1
    height = max_y + offset + 1

    for y in range(height):
        row_chars = []
        for x in range(width):
            state = point_in_polygon_grid((x, y), poly)
            row_chars.append("#" if state >= 0 else ".")
        print("".join(row_chars))

def parse_input() -> list[Point2d]:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            lines = file.readlines()
    else:
        lines = sys.stdin.readlines()

    return [tuple(map(int, line.strip().split(","))) for line in lines]  # type: ignore


def main() -> None:
    rectangles = parse_input()
    max_rect_area = calculate_max_rectangle_area(rectangles)
    print(max_rect_area)


if __name__ == "__main__":
    main()
