import random
from typing import List, Tuple, Optional

# =============================================================================
# 1. ACTIVITY SELECTION - GREEDY (Earliest Finish Time)
# =============================================================================
def activity_selection_greedy(activities: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Greedy activity selection: choose earliest finish time first.
    Activities: list of (start, finish) tuples.
    Returns: list of non-overlapping activities.
    """
    if not activities:
        return []
    
    # Sort by finish time
    sorted_activities = sorted(activities, key=lambda x: x[1])
    
    selected = [sorted_activities[0]]
    
    for start, finish in sorted_activities[1:]:
        # If start >= last finish, can add this activity
        if start >= selected[-1][1]:
            selected.append((start, finish))
    
    return selected


# =============================================================================
# 2. OTHER GREEDY RULES FOR ACTIVITY SELECTION
# =============================================================================
def activity_selection_earliest_start(activities: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Greedy rule: earliest start time first."""
    if not activities:
        return []
    
    sorted_activities = sorted(activities, key=lambda x: x[0])
    selected = [sorted_activities[0]]
    
    for start, finish in sorted_activities[1:]:
        if start >= selected[-1][1]:
            selected.append((start, finish))
    
    return selected


def activity_selection_shortest_duration(activities: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Greedy rule: shortest duration first."""
    if not activities:
        return []
    
    sorted_activities = sorted(activities, key=lambda x: x[1] - x[0])
    selected = [sorted_activities[0]]
    
    for start, finish in sorted_activities[1:]:
        if start >= selected[-1][1]:
            selected.append((start, finish))
    
    return selected


# =============================================================================
# 3. FRACTIONAL KNAPSACK
# =============================================================================
def fractional_knapsack(capacity: int, items: List[Tuple[int, int]]) -> Tuple[float, List[Tuple[int, int, float]]]:
    """
    Fractional knapsack: greedy by value/weight ratio.
    items: list of (value, weight) tuples.
    Returns: (total_value, list of (value, weight, fraction_taken))
    """
    # Calculate value/weight ratios and sort
    items_with_ratio = [(v, w, v / w) for v, w in items]
    items_with_ratio.sort(key=lambda x: x[2], reverse=True)
    
    total_value = 0.0
    total_weight = 0
    selected = []
    
    for value, weight, ratio in items_with_ratio:
        if total_weight + weight <= capacity:
            # Take entire item
            total_value += value
            total_weight += weight
            selected.append((value, weight, 1.0))
        else:
            # Take fraction of item
            remaining = capacity - total_weight
            fraction = remaining / weight
            total_value += value * fraction
            total_weight += remaining
            selected.append((value, weight, fraction))
            break
    
    return total_value, selected


# =============================================================================
# 4. 0/1 KNAPSACK - DP (Optimal Solution)
# =============================================================================
def knapsack_01_dp(capacity: int, items: List[Tuple[int, int]]) -> Tuple[int, List[int]]:
    """
    0/1 knapsack using DP.
    items: list of (value, weight) tuples.
    Returns: (max_value, list of selected item indices)
    """
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        value, weight = items[i - 1]
        for w in range(capacity + 1):
            if weight <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + value)
            else:
                dp[i][w] = dp[i - 1][w]
    
    # Reconstruct solution
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= items[i - 1][1]
    
    return dp[n][capacity], selected


# =============================================================================
# 5. 0/1 KNAPSACK - GREEDY (Value/Weight Ratio)
# =============================================================================
def knapsack_01_greedy(capacity: int, items: List[Tuple[int, int]]) -> Tuple[int, List[int]]:
    """
    0/1 knapsack using greedy (value/weight ratio).
    """
    items_with_idx = [(v, w, i) for i, (v, w) in enumerate(items)]
    items_with_idx.sort(key=lambda x: x[0] / x[1], reverse=True)
    
    total_value = 0
    total_weight = 0
    selected = []
    
    for value, weight, idx in items_with_idx:
        if total_weight + weight <= capacity:
            total_value += value
            total_weight += weight
            selected.append(idx)
    
    return total_value, selected


# =============================================================================
# MAIN TESTING
# =============================================================================
def main():
    print("=" * 80)
    print("GREEDY ALGORITHMS: ACTIVITY SELECTION & KNAPSACK")
    print("=" * 80)
    print()
    
    # =========================================================================
    # 1. ACTIVITY SELECTION - EXAMPLE
    # =========================================================================
    print("PART 1: ACTIVITY SELECTION (Greedy - Earliest Finish Time)")
    print("=" * 80)
    print()
    
    activities = [
        (1, 3),
        (2, 5),
        (4, 6),
        (5, 7),
        (6, 8),
        (8, 9),
    ]
    
    print("Activities (start, finish):")
    for i, (s, f) in enumerate(activities):
        print(f"  {i}: ({s}, {f})")
    print()
    
    selected = activity_selection_greedy(activities)
    print(f"Selected activities (earliest finish): {selected}")
    print(f"Number selected: {len(selected)}")
    print()
    
    # =========================================================================
    # 2. COMPARE THREE GREEDY RULES
    # =========================================================================
    print("PART 2: COMPARE THREE GREEDY RULES")
    print("=" * 80)
    print()
    
    # Random testing to find counterexamples
    found_ef_worse = False
    found_es_worse = False
    found_sd_worse = False
    
    for trial in range(1000):
        # Generate random activities
        n = random.randint(5, 15)
        activities = []
        for _ in range(n):
            start = random.randint(0, 20)
            finish = start + random.randint(1, 10)
            activities.append((start, finish))
        
        ef_count = len(activity_selection_greedy(activities))
        es_count = len(activity_selection_earliest_start(activities))
        sd_count = len(activity_selection_shortest_duration(activities))
        
        if es_count < ef_count and not found_es_worse:
            print(f"Trial {trial}: Earliest Start is worse than Earliest Finish")
            print(f"  Activities: {activities}")
            print(f"  Earliest Finish: {ef_count} activities")
            print(f"  Earliest Start: {es_count} activities")
            print(f"  Shortest Duration: {sd_count} activities")
            print()
            found_es_worse = True
        
        if sd_count < ef_count and not found_sd_worse:
            print(f"Trial {trial}: Shortest Duration is worse than Earliest Finish")
            print(f"  Activities: {activities}")
            print(f"  Earliest Finish: {ef_count} activities")
            print(f"  Earliest Start: {es_count} activities")
            print(f"  Shortest Duration: {sd_count} activities")
            print()
            found_sd_worse = True
        
        if found_es_worse and found_sd_worse:
            break
    
    if not found_es_worse:
        print("No counterexample found for Earliest Start in 1000 trials.")
        print("(Earliest Start often works well in practice, but is not optimal.)")
        print()
    
    if not found_sd_worse:
        print("No counterexample found for Shortest Duration in 1000 trials.")
        print("(Shortest Duration can be suboptimal on carefully crafted inputs.)")
        print()
    
    # =========================================================================
    # 3. FRACTIONAL KNAPSACK
    # =========================================================================
    print("PART 3: FRACTIONAL KNAPSACK (Greedy - Highest Value/Weight Ratio)")
    print("=" * 80)
    print()
    
    capacity = 50
    items = [
        (60, 10),
        (100, 20),
        (120, 30),
    ]
    
    print(f"Capacity: {capacity}")
    print("Items (value, weight):")
    for i, (v, w) in enumerate(items):
        ratio = v / w
        print(f"  {i}: ({v}, {w}) ratio={ratio:.2f}")
    print()
    
    frac_value, frac_items = fractional_knapsack(capacity, items)
    print(f"Fractional knapsack value: {frac_value:.2f}")
    print("Selected items (value, weight, fraction):")
    for v, w, frac in frac_items:
        print(f"  ({v}, {w}): take {frac:.2f} ({frac*w:.1f} weight, {frac*v:.1f} value)")
    print()
    
    # =========================================================================
    # 4. 0/1 KNAPSACK - GREEDY VS DP
    # =========================================================================
    print("PART 4: 0/1 KNAPSACK - GREEDY vs OPTIMAL (DP)")
    print("=" * 80)
    print()
    print(f"{'Trial':>6} {'Capacity':>10} {'Greedy':>10} {'Optimal':>10} {'Ratio':>10} {'Items':>30}")
    print("-" * 80)
    
    worst_ratio = 1.0
    worst_trial = None
    
    for trial in range(100):
        capacity = random.randint(20, 100)
        n_items = random.randint(5, 20)
        items = [(random.randint(10, 100), random.randint(5, 50)) for _ in range(n_items)]
        
        greedy_value, greedy_sel = knapsack_01_greedy(capacity, items)
        optimal_value, optimal_sel = knapsack_01_dp(capacity, items)
        
        if optimal_value > 0:
            ratio = greedy_value / optimal_value
        else:
            ratio = 1.0
        
        if ratio < worst_ratio:
            worst_ratio = ratio
            worst_trial = trial
        
        if trial < 10 or ratio < 0.95:
            items_str = f"n={n_items}"
            print(f"{trial:6d} {capacity:10d} {greedy_value:10d} {optimal_value:10d} {ratio:10.4f} {items_str:>30}")
    
    print()
    print(f"Worst ratio found: {worst_ratio:.4f}")
    print(f"(Greedy achieves {worst_ratio*100:.2f}% of optimal value)")
    print()
    
    # =========================================================================
    # ANALYSIS
    # =========================================================================
    print("=" * 80)
    print("ANALYSIS")
    print("=" * 80)
    print()
    
    print("1. ACTIVITY SELECTION")
    print("   Earliest Finish Time: OPTIMAL (greedy always works)")
    print("   Earliest Start Time: Can be suboptimal")
    print("   Shortest Duration: Can be suboptimal")
    print("   Why EFT works: Leaves maximum time for future activities")
    print()
    
    print("2. FRACTIONAL KNAPSACK")
    print("   Greedy by value/weight ratio: OPTIMAL")
    print("   Why: Can fill knapsack optimally by taking partial items")
    print("   Complexity: O(n log n) for sorting")
    print()
    
    print("3. 0/1 KNAPSACK")
    print("   Greedy by value/weight ratio: NOT OPTIMAL")
    print("   Example: Items (10, 5), (9, 4), capacity 9")
    print("   Greedy picks (10, 5) + partial, but optimal is (9, 4) + (10, 5)")
    print("   DP solution: O(n*W) time and space")
    print()
    
    print("4. KEY INSIGHT")
    print("   Greedy works for activity selection and fractional knapsack")
    print("   Greedy fails for 0/1 knapsack (no fractional items)")
    print("   0/1 knapsack requires DP due to discrete choices")
    print()


if __name__ == "__main__":
    main()
