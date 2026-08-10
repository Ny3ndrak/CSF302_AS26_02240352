"""
Question 3: Prime Number Generation - Empirical Comparison
===========================================================
Student: 02240352
1. Naive Trial Division - O(n^2) style: check every divisor up to n-1
2. Optimized Trial Division - check divisors only up to sqrt(n)
3. Sieve of Eratosthenes - O(n log log n)
"""

import time
import csv
import math

INPUT_SIZES_352 = [10_000, 50_000, 100_000, 500_000, 1_000_000]
NAIVE_TIME_BUDGET_352 = 10.0


def is_prime_naive_352(n_352):
    """Naive: Check up to n-1"""
    if n_352 < 2:
        return False
    for i_352 in range(2, n_352):
        if n_352 % i_352 == 0:
            return False
    return True


def naive_primes_352(limit_352):
    """Generate primes using naive method"""
    return [n_352 for n_352 in range(2, limit_352 + 1) if is_prime_naive_352(n_352)]


def is_prime_optimized_352(n_352):
    """Optimized: Check divisors only up to sqrt(n)"""
    if n_352 < 2:
        return False
    if n_352 in (2, 3):
        return True
    if n_352 % 2 == 0:
        return False
    r_352 = int(math.isqrt(n_352))
    for i_352 in range(3, r_352 + 1, 2):
        if n_352 % i_352 == 0:
            return False
    return True


def optimized_primes_352(limit_352):
    """Generate primes using optimized method"""
    return [n_352 for n_352 in range(2, limit_352 + 1) if is_prime_optimized_352(n_352)]


def sieve_of_eratosthenes_352(limit_352):
    """Sieve of Eratosthenes - most efficient"""
    is_p_352 = bytearray([1]) * (limit_352 + 1)
    is_p_352[0:2] = b"\x00\x00"
    for i_352 in range(2, int(math.isqrt(limit_352)) + 1):
        if is_p_352[i_352]:
            step_352 = i_352
            start_352 = i_352 * i_352
            is_p_352[start_352: limit_352 + 1: step_352] = bytearray(len(range(start_352, limit_352 + 1, step_352)))
    return [i_352 for i_352, v_352 in enumerate(is_p_352) if v_352]


def timed_352(fn_352, *args_352):
    """Measure execution time"""
    start_352 = time.perf_counter()
    result_352 = fn_352(*args_352)
    return result_352, time.perf_counter() - start_352


def main_352():
    """Main execution function"""
    results_352 = []
    naive_disabled_352 = False
    
    print("=" * 90)
    print("PRIME NUMBER GENERATION - Performance Comparison")
    print("Student: 02240352")
    print("=" * 90)
    print(f"{'N':>12} {'Primes':>10} {'Naive (sec)':>15} {'Optimized (sec)':>18} {'Sieve (sec)':>15}")
    print("-" * 90)

    for n_352 in INPUT_SIZES_352:
        row_352 = {"N": n_352}

        # Naive trial division
        if not naive_disabled_352:
            primes_naive_352, t_naive_352 = timed_352(naive_primes_352, n_352)
            row_352["naive_sec"] = t_naive_352
            naive_count_352 = len(primes_naive_352)
            if t_naive_352 > NAIVE_TIME_BUDGET_352:
                naive_disabled_352 = True
        else:
            row_352["naive_sec"] = None
            naive_count_352 = None

        # Optimized trial division
        primes_opt_352, t_opt_352 = timed_352(optimized_primes_352, n_352)
        row_352["optimized_sec"] = t_opt_352
        row_352["prime_count"] = len(primes_opt_352)

        # Sieve of Eratosthenes
        primes_sieve_352, t_sieve_352 = timed_352(sieve_of_eratosthenes_352, n_352)
        row_352["sieve_sec"] = t_sieve_352

        # Sanity check
        assert len(primes_opt_352) == len(primes_sieve_352), "Prime count mismatch!"
        if naive_count_352:
            assert naive_count_352 == row_352["prime_count"], "Naive count mismatch!"
        
        # Display results
        naive_str_352 = f"{row_352['naive_sec']:.4f}" if row_352['naive_sec'] else "SKIPPED"
        print(f"{n_352:>12,} {row_352['prime_count']:>10,} {naive_str_352:>15} {t_opt_352:>18.6f} {t_sieve_352:>15.6f}")

        results_352.append(row_352)

    with open("q3_results_352.csv", "w", newline="") as f_352:
        writer_352 = csv.DictWriter(f_352, fieldnames=["N", "prime_count", "naive_sec", "optimized_sec", "sieve_sec"])
        writer_352.writeheader()
        writer_352.writerows(results_352)

    print("=" * 90)
    print("✅ Results saved to 'q3_results_352.csv'")
    print("=" * 90)
    return results_352


if __name__ == "__main__":
    main_352()
