"""Greedy and dynamic-programming algorithms for hall booking requests."""

from bisect import bisect_right
from typing import List, Sequence, Tuple

Request = Tuple[int, int, int]
Schedule = Tuple[int, List[int]]


def _validate(requests: Sequence[Request]) -> None:
    for start, finish, fee in requests:
        if finish < start:
            raise ValueError("a request cannot finish before it starts")
        if fee < 0:
            raise ValueError("request fees must be non-negative")


def _schedule_order(requests: Sequence[Request], indices: List[int]) -> List[int]:
    return sorted(indices, key=lambda i: (requests[i][0], requests[i][1], i))


def greedy_earliest_finish(requests: Sequence[Request]) -> Schedule:
    """Accept compatible requests in ascending order of finish time."""
    _validate(requests)
    ordered = sorted(
        enumerate(requests),
        key=lambda item: (item[1][1], item[1][0], item[0]),
    )
    chosen: List[int] = []
    total_fee = 0
    last_finish = None

    for index, (start, finish, fee) in ordered:
        if last_finish is None or start >= last_finish:
            chosen.append(index)
            total_fee += fee
            last_finish = finish

    return total_fee, chosen


def greedy_highest_fee(requests: Sequence[Request]) -> Schedule:
    """Accept the highest-fee request that does not overlap accepted requests."""
    _validate(requests)
    ordered = sorted(
        enumerate(requests),
        key=lambda item: (-item[1][2], item[1][1], item[1][0], item[0]),
    )
    chosen: List[int] = []
    total_fee = 0

    for index, (start, finish, fee) in ordered:
        fits = all(
            finish <= requests[other][0] or requests[other][1] <= start
            for other in chosen
        )
        if fits:
            chosen.append(index)
            total_fee += fee

    return total_fee, _schedule_order(requests, chosen)


def best_schedule(requests: Sequence[Request]) -> Schedule:
    """Return a maximum-fee compatible schedule using weighted interval DP."""
    _validate(requests)
    ordered = sorted(
        enumerate(requests),
        key=lambda item: (item[1][1], item[1][0], item[0]),
    )
    finishes = [request[1] for _, request in ordered]
    count = len(ordered)
    optimum = [0] * (count + 1)
    predecessors = [0] * count

    for j, (index, (start, finish, fee)) in enumerate(ordered):
        predecessor_count = bisect_right(finishes, start, 0, j)
        predecessors[j] = predecessor_count
        take = fee + optimum[predecessor_count]
        skip = optimum[j]
        optimum[j + 1] = max(skip, take)

    chosen: List[int] = []
    j = count
    while j > 0:
        index, (_, _, fee) = ordered[j - 1]
        take = fee + optimum[predecessors[j - 1]]
        if take > optimum[j - 1]:
            chosen.append(index)
            j = predecessors[j - 1]
        else:
            j -= 1

    chosen.reverse()
    return optimum[count], chosen


def brute_force(requests: Sequence[Request]) -> Schedule:
    """Check all subsets; intended only for at most 15 requests."""
    _validate(requests)
    if len(requests) > 15:
        raise ValueError("brute_force supports at most 15 requests")

    ordered = sorted(
        enumerate(requests),
        key=lambda item: (item[1][0], item[1][1], item[0]),
    )
    best_fee = 0
    best_chosen: List[int] = []

    for subset in range(1 << len(ordered)):
        total_fee = 0
        chosen: List[int] = []
        last_finish = None
        compatible = True

        for position, (index, (start, finish, fee)) in enumerate(ordered):
            if not (subset & (1 << position)):
                continue
            if last_finish is not None and start < last_finish:
                compatible = False
                break
            chosen.append(index)
            total_fee += fee
            last_finish = finish

        if compatible and total_fee > best_fee:
            best_fee = total_fee
            best_chosen = chosen

    return best_fee, best_chosen
