"""
Question 1: Linear Search vs Binary Search
============================================
Student: 02240352
This program compares the performance of Linear Search (O(n)) and Binary Search (O(log n)).
"""

import random
import time
import csv

# Configuration
INPUT_SIZES_352 = [1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]
TRIALS_352 = 7
TARGETS_PER_TRIAL_352 = 20

random.seed(42)


def linear_search_352(data_352, target_352):
    """
    Linear Search Algorithm - O(n)
    Scans through the array from start to end until target is found.
    Returns the index if found, otherwise -1.
    """
    for i_352 in range(len(data_352)):
        if data_352[i_352] == target_352:
            return i_352
    return -1


def binary_search_352(data_352, target_352):
    """
    Binary Search Algorithm - O(log n)
    Requires SORTED data. Works by repeatedly dividing the search space in half.
    Returns the index if found, otherwise -1.
    """
    left_352, right_352 = 0, len(data_352) - 1
    
    while left_352 <= right_352:
        middle_352 = (left_352 + right_352) // 2
        
        if data_352[middle_352] == target_352:
            return middle_352
        elif data_352[middle_352] < target_352:
            left_352 = middle_352 + 1
        else:
            right_352 = middle_352 - 1
    
    return -1


def generate_dataset_352(size_352):
    """
    Creates a random dataset of the specified size.
    Values range from 0 to size*10 to make duplicates rare.
    """
    return [random.randint(0, size_352 * 10) for _ in range(size_352)]


def measure_search_time_352(search_function_352, data_352, targets_352, trials_352):
    """
    Measures the average time to perform a search across multiple trials.
    Returns: Average time in seconds per individual search
    """
    start_time_352 = time.perf_counter()
    
    for _ in range(trials_352):
        for target_352 in targets_352:
            search_function_352(data_352, target_352)
    
    end_time_352 = time.perf_counter()
    total_time_352 = end_time_352 - start_time_352
    
    return total_time_352 / (trials_352 * len(targets_352))


def main_352():
    """Main execution function that runs the performance comparison."""
    results_352 = []
    
    print("=" * 80)
    print("LINEAR SEARCH vs BINARY SEARCH - Performance Comparison")
    print("Student: 02240352")
    print("=" * 80)
    print(f"{'Dataset Size':>15} {'Linear (sec)':>15} {'Binary (sec)':>15} {'Sort (sec)':>13}")
    print("-" * 80)
    
    for size_352 in INPUT_SIZES_352:
        print(f"Generating dataset of {size_352:,} elements...", end=" ", flush=True)
        
        # Step 1: Generate random dataset
        dataset_352 = generate_dataset_352(size_352)
        
        # Step 2: Prepare search targets
        half_352 = TARGETS_PER_TRIAL_352 // 2
        existing_targets_352 = random.sample(dataset_352, half_352)
        random_targets_352 = [random.randint(0, size_352 * 10) for _ in range(TARGETS_PER_TRIAL_352 - half_352)]
        targets_352 = existing_targets_352 + random_targets_352
        
        # Step 3: Test Linear Search
        print("linear...", end=" ", flush=True)
        linear_avg_time_352 = measure_search_time_352(linear_search_352, dataset_352, targets_352, TRIALS_352)
        
        # Step 4: Sort the dataset
        print("sorting...", end=" ", flush=True)
        sort_start_352 = time.perf_counter()
        sorted_dataset_352 = sorted(dataset_352)
        sort_time_352 = time.perf_counter() - sort_start_352
        
        # Step 5: Test Binary Search
        print("binary...", end=" ", flush=True)
        binary_avg_time_352 = measure_search_time_352(binary_search_352, sorted_dataset_352, targets_352, TRIALS_352)
        
        # Step 6: Record results
        results_352.append({
            "n": size_352,
            "linear_search_avg_sec": linear_avg_time_352,
            "binary_search_avg_sec": binary_avg_time_352,
            "sort_time_sec": sort_time_352,
        })
        
        # Display progress
        print("done!")
        print(f"{size_352:>15,} {linear_avg_time_352:>15.8f} {binary_avg_time_352:>15.10f} {sort_time_352:>13.4f}")
        print()
    
    # Step 7: Save results to CSV
    with open("q1_results_352.csv", "w", newline="") as csv_file_352:
        writer_352 = csv.DictWriter(csv_file_352, fieldnames=["n", "linear_search_avg_sec", "binary_search_avg_sec", "sort_time_sec"])
        writer_352.writeheader()
        writer_352.writerows(results_352)
    
    print("=" * 80)
    print("✅ Results saved to 'q1_results_352.csv'")
    print("=" * 80)
    
    return results_352


if __name__ == "__main__":
    main_352()
