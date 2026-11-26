"""Closest-pair algorithms for two-dimensional points."""

from math import sqrt
from typing import Dict, List, Sequence, Tuple

Point = Tuple[float, float]
Result = Tuple[float, int, int]
_IndexedPoint = Tuple[float, float, int]
_Candidate = Tuple[float, int, int]


def _validate(points: Sequence[Point]) -> None:
    if len(points) < 2:
        raise ValueError("at least two points are required")


def _squared_distance(a: _IndexedPoint, b: _IndexedPoint) -> float:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


def closest_pair_brute(points: Sequence[Point]) -> Result:
    """Return the closest distance and its original point indices in Θ(n²)."""
    _validate(points)
    best: _Candidate = (float("inf"), -1, -1)

    for i in range(len(points) - 1):
        a = (points[i][0], points[i][1], i)
        for j in range(i + 1, len(points)):
            b = (points[j][0], points[j][1], j)
            candidate = (_squared_distance(a, b), i, j)
            if candidate < best:
                best = candidate

    return sqrt(best[0]), best[1], best[2]


def closest_pair(points: Sequence[Point]) -> Result:
    """Return the closest pair using an O(n log n) divide-and-conquer method."""
    _validate(points)
    indexed = [(point[0], point[1], i) for i, point in enumerate(points)]

    # Resolve zero-distance pairs first; this also keeps the strip scan bounded.
    first_at_coordinate: Dict[Point, int] = {}
    duplicate_best: Tuple[int, int] = (len(points), len(points))
    for i, point in enumerate(points):
        first = first_at_coordinate.get(point)
        if first is None:
            first_at_coordinate[point] = i
        else:
            duplicate_best = min(duplicate_best, (first, i))
    if duplicate_best[0] < len(points):
        return 0.0, duplicate_best[0], duplicate_best[1]

    by_x = sorted(indexed, key=lambda point: (point[0], point[1], point[2]))
    by_y = sorted(indexed, key=lambda point: (point[1], point[0], point[2]))

    def solve(x_order: List[_IndexedPoint], y_order: List[_IndexedPoint]) -> _Candidate:
        if len(x_order) <= 3:
            best: _Candidate = (float("inf"), -1, -1)
            for i in range(len(x_order) - 1):
                for j in range(i + 1, len(x_order)):
                    a = x_order[i]
                    b = x_order[j]
                    candidate = (_squared_distance(a, b), min(a[2], b[2]), max(a[2], b[2]))
                    if candidate < best:
                        best = candidate
            return best

        middle = len(x_order) // 2
        left_x = x_order[:middle]
        right_x = x_order[middle:]
        left_indices = {point[2] for point in left_x}
        left_y: List[_IndexedPoint] = []
        right_y: List[_IndexedPoint] = []
        for point in y_order:
            if point[2] in left_indices:
                left_y.append(point)
            else:
                right_y.append(point)

        best = min(solve(left_x, left_y), solve(right_x, right_y))
        dividing_x = (left_x[-1][0] + right_x[0][0]) / 2
        strip = [
            point for point in y_order
            if (point[0] - dividing_x) ** 2 <= best[0]
        ]

        for i, point in enumerate(strip):
            # At most seven following points can be closer in a δ-wide strip.
            for j in range(i + 1, min(i + 8, len(strip))):
                other = strip[j]
                if (other[1] - point[1]) ** 2 > best[0]:
                    break
                if (point[2] in left_indices) == (other[2] in left_indices):
                    continue
                candidate = (
                    _squared_distance(point, other),
                    min(point[2], other[2]),
                    max(point[2], other[2]),
                )
                if candidate < best:
                    best = candidate

        return best

    best = solve(by_x, by_y)
    return sqrt(best[0]), best[1], best[2]
