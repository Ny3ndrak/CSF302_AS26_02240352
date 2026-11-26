"""Quicksort implementations for the Assignment 3 transaction data."""

import random
from typing import List


def quicksort_basic(a: List[int]) -> None:
    """Sort a in place using last-element Lomuto quicksort."""

    def sort(low: int, high: int) -> None:
        if low >= high:
            return

        pivot = a[high]
        boundary = low
        for current in range(low, high):
            if a[current] < pivot:
                a[boundary], a[current] = a[current], a[boundary]
                boundary += 1
        a[boundary], a[high] = a[high], a[boundary]
        sort(low, boundary - 1)
        sort(boundary + 1, high)

    sort(0, len(a) - 1)


def quicksort_improved(a: List[int], cutoff: int = 16) -> None:
    """Sort a in place using randomized three-way quicksort and insertion sort."""
    if cutoff < 1:
        raise ValueError("cutoff must be at least 1")

    def insertion_sort(low: int, high: int) -> None:
        for current in range(low + 1, high + 1):
            value = a[current]
            position = current - 1
            while position >= low and a[position] > value:
                a[position + 1] = a[position]
                position -= 1
            a[position + 1] = value

    def sort(low: int, high: int) -> None:
        while low < high:
            if high - low + 1 <= cutoff:
                insertion_sort(low, high)
                return

            pivot = a[random.randrange(low, high + 1)]
            less = low
            current = low
            greater = high

            while current <= greater:
                if a[current] < pivot:
                    a[less], a[current] = a[current], a[less]
                    less += 1
                    current += 1
                elif a[current] > pivot:
                    a[current], a[greater] = a[greater], a[current]
                    greater -= 1
                else:
                    current += 1

            left_size = less - low
            right_size = high - greater
            if left_size < right_size:
                sort(low, less - 1)
                low = greater + 1
            else:
                sort(greater + 1, high)
                high = less - 1

    sort(0, len(a) - 1)
