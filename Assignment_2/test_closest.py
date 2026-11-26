"""Tests for the closest-pair implementations."""

import random
import unittest

from closest import closest_pair, closest_pair_brute


class ClosestPairTests(unittest.TestCase):
    def test_exactly_two_points(self):
        points = [(2, 3), (3, 4)]
        self.assertEqual(closest_pair(points), (2 ** 0.5, 0, 1))

    def test_duplicate_points_return_zero_and_smallest_indices(self):
        points = [(0, 0), (2, 2), (0, 0), (0, 0)]
        self.assertEqual(closest_pair(points), (0.0, 0, 2))
        self.assertEqual(closest_pair(points), closest_pair_brute(points))

    def test_vertical_line(self):
        points = [(7, 10), (7, -2), (7, 3), (7, 4)]
        self.assertEqual(closest_pair(points), closest_pair_brute(points))
        self.assertEqual(closest_pair(points), (1.0, 2, 3))

    def test_closest_pair_crosses_dividing_line(self):
        points = [(0, 0), (3, 2), (4, 0), (5, 5)]
        self.assertEqual(closest_pair(points), closest_pair_brute(points))
        self.assertEqual(closest_pair(points)[1:], (1, 2))

    def test_random_inputs_match_brute_force(self):
        generator = random.Random(302)
        for _ in range(500):
            count = generator.randint(2, 50)
            points = [
                (generator.randint(-100, 100), generator.randint(-100, 100))
                for _ in range(count)
            ]
            with self.subTest(case=_):
                self.assertEqual(closest_pair(points), closest_pair_brute(points))

    def test_rejects_fewer_than_two_points(self):
        for function in (closest_pair, closest_pair_brute):
            with self.subTest(function=function.__name__):
                with self.assertRaises(ValueError):
                    function([(0, 0)])


if __name__ == "__main__":
    unittest.main()
