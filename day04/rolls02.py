from collections import deque
import sys
from typing import Literal, NamedTuple, cast

type GridItem = Literal[".", "@", "X"]
type Grid = list[list[GridItem]]


class Neighbor(NamedTuple):
    item: GridItem
    coord: tuple[int, int]


class Grid1DPadded:
    def __init__(self, grid: list[list[GridItem]]) -> None:
        self.width = len(grid[0])
        self.height = len(grid)
        self.size = self.width * self.height
        self._stride = self.width + 2
        self._total_size = self._stride * (self.height + 2)

        # first row of padding
        self._grid_1d: list[GridItem] = ["."] * self._stride

        for y in range(self.height):
            self._grid_1d.extend(["."] + grid[y] + ["."])  # type: ignore

        # last row of padding
        self._grid_1d.extend(["."] * self._stride)  # type: ignore

        s = self._stride
        self._offsets = (
            -s - 1,  # Top-Left
            -s,  # top
            -s + 1,  # Top-Right
            -1,  # Left
            1,  # Right
            s - 1,  # Bottom-Left
            s,  # Bottom
            s + 1,  # Bottom-Right
        )

    def get(self, x: int, y: int) -> GridItem:
        """Coordinates are from original grid."""
        return self._grid_1d[(y + 1) * self._stride + (x + 1)]

    def get_neighbors(self, x: int, y: int) -> list[Neighbor]:
        """Coordinates are from original grid."""

        center_idx = (y + 1) * self._stride + (x + 1)

        return [
            Neighbor(self._grid_1d[center_idx + offset], (x + dx, y + dy))
            for offset, (dx, dy) in zip(
                self._offsets,
                [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)],
            )
        ]

    def set(self, x: int, y: int, value: GridItem) -> None:
        """Coordinates are from original grid."""
        self._grid_1d[(y + 1) * self._stride + (x + 1)] = value

    def __repr__(self) -> str:
        lines = []
        for y in range(self.height):
            line = "".join(
                self._grid_1d[
                    (y + 1) * self._stride + 1 : (y + 1) * self._stride + 1 + self.width
                ]
            )
            lines.append(line)
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.__repr__()


def count_fork_accessible_rolls(grid2d: Grid) -> int:
    grid = Grid1DPadded(grid2d)

    q: deque[tuple[int, int]] = deque()
    for y in range(grid.height):
        for x in range(grid.width):
            if grid.get(x, y) == "@":
                q.append((x, y))

    count = 0

    while q:
        x, y = q.popleft()

        if grid.get(x, y) != "@":
            continue

        neighbor_rolls = grid.get_neighbors(x, y)
        neighbor_rolls_count = sum(
            1 for neighbor in neighbor_rolls if neighbor.item == "@"
        )

        if neighbor_rolls_count < 4:
            grid.set(x, y, "X")
            count += 1

            # Enqueue neighbors to re-check
            q.extend(
                neighbor.coord for neighbor in neighbor_rolls if neighbor.item == "@"
            )

    return count


def parse_input() -> list[list[GridItem]]:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            lines = file.readlines()
    else:
        lines = sys.stdin.readlines()

    return [[cast(GridItem, char) for char in line.strip()] for line in lines]


def main() -> None:
    lines = parse_input()
    result = count_fork_accessible_rolls(lines)
    print(result)


if __name__ == "__main__":
    main()
