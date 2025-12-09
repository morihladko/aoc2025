import math
import sys

type Box = tuple[int, int, int]
type Point3d = tuple[float | int, float | int, float | int]


def calculate_3d_distance(point1: Point3d, point2: Point3d) -> float:
    return math.sqrt(
        (point2[0] - point1[0]) ** 2
        + (point2[1] - point1[1]) ** 2
        + (point2[2] - point1[2]) ** 2
    )


def calculate_distances(boxes: list[Box]) -> dict[str, float]:
    """
    >>> calculate_distances([(0, 0, 0), (2, 3, 6), (-2, 3, 6)])
    {'0-1': 7.0, '0-2': 7.0, '1-2': 4.0}
    """
    distances = {}
    for i, box in enumerate(boxes[:-1]):
        for j, other_box in enumerate(boxes[i + 1 :], start=i + 1):
            distances[f"{i}-{j}"] = calculate_3d_distance(box, other_box)
    return distances


def multiply_largest_circuits(juction_boxes: list[Box]) -> int:
    # box id is the index in juction_boxes
    distances = calculate_distances(juction_boxes)
    circuits = list([i] for i in range(len(juction_boxes)))
    sorted_distances = sorted(distances.items(), key=lambda item: item[1], reverse=True)

    while True:
        key, _ = sorted_distances.pop()
        box1_id, box2_id = map(int, key.split("-"))
        circuit_1 = next(circuit for circuit in circuits if box1_id in circuit)
        circuit_2 = next(circuit for circuit in circuits if box2_id in circuit)

        if circuit_1 is circuit_2:
            continue

        circuit_1.extend(circuit_2)
        circuits.remove(circuit_2)

        if len(circuits) == 1:
            box_1 = juction_boxes[box1_id]
            box_2 = juction_boxes[box2_id]

            return box_1[0] * box_2[0]


def parse_input() -> list[Box]:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            lines = file.readlines()
    else:
        lines = sys.stdin.readlines()

    return [tuple(map(int, line.strip().split(","))) for line in lines]  # type: ignore


def main() -> None:
    boxes = parse_input()
    result = multiply_largest_circuits(boxes)
    print(result)


if __name__ == "__main__":
    main()
