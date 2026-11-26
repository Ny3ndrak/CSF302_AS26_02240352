"""Tests for the Assignment 3 sorting implementations."""

import random
import unittest

from sorts import quicksort_basic, quicksort_improved


class QuicksortTests(unittest.TestCase):
    def test_required_edge_cases(self):
        examples = (
            [],
            [7],
            [4, 4, 4, 4],
            list(range(100)),
            list(range(100, 0, -1)),
            [0, -3, 8, -1, 5, -9],
        )
        for sort in (quicksort_basic, quicksort_improved):
            for example in examples:
                with self.subTest(sort=sort.__name__, values=example[:5]):
                    values = example.copy()
                    sort(values)
                    self.assertEqual(values, sorted(example))

    def test_500_random_lists_against_sorted(self):
        generator = random.Random(503)
        for case in range(500):
            values = [
                generator.randint(-1000, 1000)
                for _ in range(generator.randint(0, 100))
            ]
            expected = sorted(values)
            for sort in (quicksort_basic, quicksort_improved):
                result = values.copy()
                with self.subTest(case=case, sort=sort.__name__):
                    sort(result)
                    self.assertEqual(result, expected)

    def test_improved_handles_large_organized_and_duplicate_inputs(self):
        examples = [
            list(range(20_000)),
            list(range(20_000, 0, -1)),
            [i % 10 for i in range(20_000)],
        ]
        for values in examples:
            expected = sorted(values)
            quicksort_improved(values)
            self.assertEqual(values, expected)

    def test_all_benchmarked_cutoffs_sort_correctly(self):
        generator = random.Random(316)
        original = [generator.randint(-50, 50) for _ in range(2_000)]
        expected = sorted(original)
        for cutoff in (1, 4, 8, 16, 32, 64):
            with self.subTest(cutoff=cutoff):
                values = original.copy()
                quicksort_improved(values, cutoff=cutoff)
                self.assertEqual(values, expected)

    def test_cutoff_must_be_positive(self):
        with self.assertRaises(ValueError):
            quicksort_improved([2, 1], cutoff=0)


if __name__ == "__main__":
    unittest.main()
