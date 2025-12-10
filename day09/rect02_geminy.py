import sys
from itertools import combinations

# Type alias for clarity
type Point2d = tuple[int, int]


def parse_input() -> list[Point2d]:
    """Reads coordinate pairs from file or stdin."""
    lines = []
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            lines = file.readlines()
    else:
        lines = sys.stdin.readlines()

    # Filter out empty lines and parse
    points = []
    for line in lines:
        line = line.strip()
        if line:
            parts = line.split(",")
            points.append((int(parts[0]), int(parts[1])))
    return points


def is_point_in_polygon(x: float, y: float, poly: list[Point2d]) -> bool:
    """
    Ray casting algorithm to check if a point (x, y) is inside or on the boundary.
    Supports float coordinates (for checking rectangle centers).
    """
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]

        # Ray casting logic
        if (y1 > y) != (y2 > y):
            # Calculate intersection of the edge with the ray
            intersect_x = (x2 - x1) * (y - y1) / (y2 - y1) + x1
            if x < intersect_x:
                inside = not inside
    return inside


def edge_intersects_rect(
    r_x1: int, r_y1: int, r_x2: int, r_y2: int, poly: list[Point2d]
) -> bool:
    """
    Checks if any polygon edge strictly intersects the interior of the rectangle.

    Rectangle range: x in [min_x, max_x], y in [min_y, max_y]
    Strict intersection means the edge passes through the open interval (min_x, max_x) x (min_y, max_y).
    """
    min_x, max_x = min(r_x1, r_x2), max(r_x1, r_x2)
    min_y, max_y = min(r_y1, r_y2), max(r_y1, r_y2)

    n = len(poly)
    for i in range(n):
        px1, py1 = poly[i]
        px2, py2 = poly[(i + 1) % n]

        # Check Vertical Edge (px1 == px2)
        if px1 == px2:
            # Does the X coordinate fall strictly inside the rectangle's X range?
            if min_x < px1 < max_x:
                # Does the edge's Y range overlap with the rectangle's interior Y range?
                edge_y_min, edge_y_max = min(py1, py2), max(py1, py2)
                # Overlap check of open intervals (min_y, max_y) and (edge_y_min, edge_y_max)
                if max(min_y, edge_y_min) < min(max_y, edge_y_max):
                    return True  # Cut detected

        # Check Horizontal Edge (py1 == py2)
        elif py1 == py2:
            # Does the Y coordinate fall strictly inside the rectangle's Y range?
            if min_y < py1 < max_y:
                # Does the edge's X range overlap with the rectangle's interior X range?
                edge_x_min, edge_x_max = min(px1, px2), max(px1, px2)
                if max(min_x, edge_x_min) < min(max_x, edge_x_max):
                    return True  # Cut detected

    return False


def main() -> None:
    poly = parse_input()
    if not poly:
        return

    max_area = 0

    # Iterate all pairs of vertices to form candidate rectangles
    # Optimization: Filter degenerate pairs if necessary, but formula handles them.
    for p1, p2 in combinations(poly, 2):
        x1, y1 = p1
        x2, y2 = p2

        # Calculate Tile Area immediately to prune small rectangles
        # Area = (width_tiles) * (height_tiles)
        current_area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)

        if current_area <= max_area:
            continue

        # --- Validation Steps ---

        # 1. Center Check
        # We check the geometric center of the rectangle.
        # This handles cases like "U" shapes where the corners are valid but the middle is empty space.
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        if not is_point_in_polygon(center_x, center_y, poly):
            continue

        # 2. Edge Intersection Check
        # We ensure no polygon boundary cuts through the rectangle.
        # This handles holes inside the rectangle or complex shapes.
        if edge_intersects_rect(x1, y1, x2, y2, poly):
            continue

        # If passed both checks, it is a valid sub-rectangle
        max_area = current_area

    print(max_area)


if __name__ == "__main__":
    main()
