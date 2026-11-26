"""Tests for the hall-booking scheduling algorithms."""

import random
import unittest

from booking import (
    best_schedule,
    brute_force,
    greedy_earliest_finish,
    greedy_highest_fee,
)


def is_compatible(requests, indices):
    ordered = sorted(indices, key=lambda i: (requests[i][0], requests[i][1]))
    return all(
        requests[left][1] <= requests[right][0]
        for left, right in zip(ordered, ordered[1:])
    )


class BookingTests(unittest.TestCase):
    def test_required_edge_cases(self):
        examples = (
            [],
            [(2, 4, 10)],
            [(1, 5, 10), (2, 6, 20), (3, 7, 30)],
            [(1, 2, 3), (2, 3, 4), (3, 4, 5)],
            [(1, 3, 5), (3, 4, 7), (4, 8, 9)],
        )
        for requests in examples:
            with self.subTest(requests=requests):
                expected_fee, chosen = best_schedule(requests)
                self.assertEqual((expected_fee, chosen), brute_force(requests))
                for algorithm in (greedy_earliest_finish, greedy_highest_fee):
                    fee, selection = algorithm(requests)
                    self.assertEqual(fee, sum(requests[i][2] for i in selection))
                    self.assertTrue(is_compatible(requests, selection))

    def test_500_random_inputs_match_brute_force(self):
        generator = random.Random(604)
        for case in range(500):
            requests = []
            for _ in range(generator.randint(0, 10)):
                start = generator.randint(0, 20)
                finish = generator.randint(start, start + 8)
                fee = generator.randint(0, 1000)
                requests.append((start, finish, fee))

            expected_fee, _ = brute_force(requests)
            actual_fee, chosen = best_schedule(requests)
            with self.subTest(case=case):
                self.assertEqual(actual_fee, expected_fee)
                self.assertEqual(actual_fee, sum(requests[i][2] for i in chosen))
                self.assertTrue(is_compatible(requests, chosen))

    def test_earliest_finish_is_optimal_when_fees_are_equal(self):
        generator = random.Random(607)
        for case in range(500):
            fee = generator.randint(0, 100)
            requests = []
            for _ in range(generator.randint(0, 10)):
                start = generator.randint(0, 20)
                finish = generator.randint(start, start + 8)
                requests.append((start, finish, fee))

            self.assertEqual(
                greedy_earliest_finish(requests)[0],
                best_schedule(requests)[0],
                msg=f"case {case}: {requests}",
            )

    def test_greedy_counterexample(self):
        requests = [
            (0, 2, 1),
            (1, 3, 6),
            (3, 4, 6),
            (0, 4, 10),
        ]
        optimum = best_schedule(requests)[0]
        self.assertEqual(optimum, 12)
        self.assertLess(greedy_earliest_finish(requests)[0], optimum)
        self.assertLess(greedy_highest_fee(requests)[0], optimum)

    def test_back_to_back_requests_are_compatible(self):
        requests = [(9, 12, 3), (12, 14, 4), (14, 18, 5)]
        for algorithm in (
            greedy_earliest_finish,
            greedy_highest_fee,
            best_schedule,
            brute_force,
        ):
            self.assertEqual(algorithm(requests)[0], 12)

    def test_rejects_invalid_request_and_brute_force_size(self):
        with self.assertRaises(ValueError):
            best_schedule([(5, 4, 10)])
        with self.assertRaises(ValueError):
            best_schedule([(1, 2, -1)])
        with self.assertRaises(ValueError):
            brute_force([(i, i + 1, 1) for i in range(16)])


if __name__ == "__main__":
    unittest.main()
