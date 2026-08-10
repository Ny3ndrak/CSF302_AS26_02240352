"""
Question 2: Bubble Sort vs Merge Sort
======================================
Student: 02240352
Implements both algorithms and measures average execution time.
"""

import random
import time
import csv

random.seed(42)

INPUT_SIZES_352 = [100, 500, 1000, 2000, 4000, 8000]


def bubble_sort_352(arr_352):
    """Bubble Sort - O(n^2)"""
    a_352 = arr_352[:]
    n_352 = len(a_352)
    for i_352 in range(n_352 - 1):
        swapped_352 = False
        for j_352 in range(n_352 - 1 - i_352):
            if a_352[j_352] > a_352[j_352 + 1]:
                a_352[j_352], a_352[j_352 + 1] = a_352[j_352 + 1], a_352[j_352]
                swapped_352 = True
        if not swapped_352:
            break
    return a_352


def merge_sort_352(arr_352):
    """Merge Sort - O(n log n)"""
    if len(arr_352) <= 1:
        return arr_352[:]
    mid_352 = len(arr_352) // 2
    left_352 = merge_sort_352(arr_352[:mid_352])
    right_352 = merge_sort_352(arr_352[mid_352:])
    return merge_352(left_352, right_352)


def merge_352(left_352, right_352):
    """Helper function to merge two sorted arrays"""
    result_352 = []
    i_352 = j_352 = 0
    while i_352 < len(left_352) and j_352 < len(right_352):
        if left_352[i_352] <= right_352[j_352]:
            result_352.append(left_352[i_352])
            i_352 += 1
        else:
            result_352.append(right_352[j_352])
            j_352 += 1
    result_352.extend(left_352[i_352:])
    result_352.extend(right_352[j_352:])
    return result_352


def make_dataset_352(n_352):
    """Generate random dataset"""
    return [random.randint(0, n_352 * 10) for _ in range(n_352)]


def trials_for_size_352(n_352):
    """Determine number of trials based on size"""
    if n_352 <= 500:
        return 15
    elif n_352 <= 2000:
        return 7
    elif n_352 <= 4000:
        return 4
    else:
        return 3


def average_time_352(sort_fn_352, datasets_352):
    """Calculate average sorting time"""
    total_352 = 0.0
    for d_352 in datasets_352:
        start_352 = time.perf_counter()
        sort_fn_352(d_352)
        total_352 += (time.perf_counter() - start_352)
    return total_352 / len(datasets_352)


def main_352():
    """Main execution function"""
    results_352 = []
    
    print("=" * 70)
    print("BUBBLE SORT vs MERGE SORT - Performance Comparison")
    print("Student: 02240352")
    print("=" * 70)
    
    for n_352 in INPUT_SIZES_352:
        trials_352 = trials_for_size_352(n_352)
        print(f"n = {n_352:,}  (trials={trials_352}) ...", flush=True)

        datasets_352 = [make_dataset_352(n_352) for _ in range(trials_352)]

        bubble_avg_352 = average_time_352(bubble_sort_352, datasets_352)
        merge_avg_352 = average_time_352(merge_sort_352, datasets_352)
        speedup_352 = bubble_avg_352 / merge_avg_352 if merge_avg_352 > 0 else None

        results_352.append({
            "n": n_352,
            "trials": trials_352,
            "bubble_sort_avg_sec": bubble_avg_352,
            "merge_sort_avg_sec": merge_avg_352,
            "speedup_factor": speedup_352,
        })
        print(f"   Bubble: {bubble_avg_352:.6f}s  |  Merge: {merge_avg_352:.6f}s  |  Speedup: {speedup_352:.1f}x")

    with open("q2_results_352.csv", "w", newline="") as f_352:
        writer_352 = csv.DictWriter(f_352, fieldnames=["n", "trials", "bubble_sort_avg_sec", "merge_sort_avg_sec", "speedup_factor"])
        writer_352.writeheader()
        writer_352.writerows(results_352)

    print("=" * 70)
    print("✅ Results saved to 'q2_results_352.csv'")
    print("=" * 70)
    return results_352


if __name__ == "__main__":
    main_352()
