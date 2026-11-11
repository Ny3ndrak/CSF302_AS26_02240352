import time
from typing import List, Tuple, Dict

# Price table: p[i] = price for length i
prices = {1: 1, 2: 5, 3: 8, 4: 9, 5: 10, 6: 17, 7: 17, 8: 20, 9: 24, 10: 30}

class CallCounter:
    """Tracks recursive calls."""
    def __init__(self):
        self.count = 0
    
    def reset(self):
        self.count = 0

call_counter = CallCounter()

# =============================================================================
# 1. NAIVE RECURSIVE SOLUTION
# =============================================================================
def cut_rod_naive(prices: Dict[int, int], n: int) -> int:
    """
    Naive recursive solution.
    Time: O(2^n), Space: O(n) for recursion stack
    """
    call_counter.count += 1
    
    if n == 0:
        return 0
    
    max_revenue = 0
    for i in range(1, n + 1):
        if i in prices:
            revenue = prices[i] + cut_rod_naive(prices, n - i)
            max_revenue = max(max_revenue, revenue)
    
    return max_revenue


# =============================================================================
# 2. TOP-DOWN MEMOIZED SOLUTION
# =============================================================================
def cut_rod_memoized(prices: Dict[int, int], n: int, memo: Dict[int, int] = None) -> int:
    """
    Top-down memoized solution.
    Time: O(n²), Space: O(n) for memo table
    """
    if memo is None:
        memo = {}
    
    call_counter.count += 1
    
    if n in memo:
        return memo[n]
    
    if n == 0:
        return 0
    
    max_revenue = 0
    for i in range(1, n + 1):
        if i in prices:
            revenue = prices[i] + cut_rod_memoized(prices, n - i, memo)
            max_revenue = max(max_revenue, revenue)
    
    memo[n] = max_revenue
    return max_revenue


# =============================================================================
# 3. BOTTOM-UP TABULATED SOLUTION
# =============================================================================
def cut_rod_tabulated(prices: Dict[int, int], n: int) -> Tuple[int, List[int]]:
    """
    Bottom-up tabulated solution with solution reconstruction.
    Time: O(n²), Space: O(n)
    Returns: (max_revenue, list of piece lengths)
    """
    dp = [0] * (n + 1)
    solution = [0] * (n + 1)
    
    for i in range(1, n + 1):
        max_revenue = 0
        best_cut = 0
        for j in range(1, i + 1):
            if j in prices:
                revenue = prices[j] + dp[i - j]
                if revenue > max_revenue:
                    max_revenue = revenue
                    best_cut = j
        dp[i] = max_revenue
        solution[i] = best_cut
    
    # Reconstruct solution
    pieces = []
    length = n
    while length > 0:
        cut = solution[length]
        pieces.append(cut)
        length -= cut
    
    return dp[n], pieces


# =============================================================================
# 4. PRINT RESULTS FOR n=1 TO 10
# =============================================================================
def print_results_small():
    print("=" * 80)
    print("ROD CUTTING RESULTS (n = 1 to 10)")
    print("=" * 80)
    print(f"{'n':>3} {'Max Revenue':>15} {'Piece Lengths':>30}")
    print("-" * 80)
    
    for n in range(1, 11):
        revenue, pieces = cut_rod_tabulated(prices, n)
        pieces_str = str(pieces)
        print(f"{n:3d} {revenue:15d} {pieces_str:>30}")
    
    print()


# =============================================================================
# 5. TIMING & CALL COUNT COMPARISON
# =============================================================================
def extend_prices(max_length: int) -> Dict[int, int]:
    """Extend price table: p[i] = 3*i for i > 10."""
    extended = prices.copy()
    for i in range(11, max_length + 1):
        extended[i] = 3 * i
    return extended


def benchmark():
    print("=" * 80)
    print("PERFORMANCE ANALYSIS (n = 5, 10, 15, 20, 25)")
    print("=" * 80)
    print()
    
    extended_prices = extend_prices(25)
    sizes = [5, 10, 15, 20, 25]
    
    results = []
    
    for n in sizes:
        print(f"Computing for n = {n}...")
        
        # 1. Naive recursive
        call_counter.reset()
        start = time.time()
        try:
            rev_naive = cut_rod_naive(extended_prices, n)
            time_naive = (time.time() - start) * 1000
            calls_naive = call_counter.count
        except RecursionError:
            rev_naive = None
            time_naive = None
            calls_naive = "RecursionError"
        
        # 2. Top-down memoized
        call_counter.reset()
        start = time.time()
        rev_memo = cut_rod_memoized(extended_prices, n)
        time_memo = (time.time() - start) * 1000
        calls_memo = call_counter.count
        
        # 3. Bottom-up tabulated
        start = time.time()
        rev_tab, _ = cut_rod_tabulated(extended_prices, n)
        time_tab = (time.time() - start) * 1000
        calls_tab = n * (n + 1) // 2 + 1  # Approximate: no actual recursion
        
        results.append({
            'n': n,
            'rev_naive': rev_naive,
            'calls_naive': calls_naive,
            'time_naive': time_naive,
            'rev_memo': rev_memo,
            'calls_memo': calls_memo,
            'time_memo': time_memo,
            'rev_tab': rev_tab,
            'calls_tab': calls_tab,
            'time_tab': time_tab,
        })
    
    print()
    print("=" * 80)
    print("RECURSIVE CALL COUNTS")
    print("=" * 80)
    print(f"{'n':>5} {'Naive':>15} {'Memoized':>15} {'Tabulated':>15} {'Naive/Memo':>15}")
    print("-" * 80)
    
    for r in results:
        n = r['n']
        calls_naive = r['calls_naive']
        calls_memo = r['calls_memo']
        calls_tab = r['calls_tab']
        
        if isinstance(calls_naive, int):
            ratio = calls_naive / calls_memo if calls_memo > 0 else 0
            ratio_str = f"{ratio:8.2f}x"
            print(f"{n:5d} {calls_naive:15d} {calls_memo:15d} {calls_tab:15d} {ratio_str:>15}")
        else:
            print(f"{n:5d} {'RecError':>15} {calls_memo:15d} {calls_tab:15d} {'N/A':>15}")
    
    print()
    print("=" * 80)
    print("EXECUTION TIME (milliseconds)")
    print("=" * 80)
    print(f"{'n':>5} {'Naive (ms)':>15} {'Memoized (ms)':>15} {'Tabulated (ms)':>15} {'Naive/Tab':>15}")
    print("-" * 80)
    
    for r in results:
        n = r['n']
        time_naive = r['time_naive']
        time_memo = r['time_memo']
        time_tab = r['time_tab']
        
        if time_naive is not None:
            ratio = time_naive / time_tab if time_tab > 0 else 0
            ratio_str = f"{ratio:8.2f}x"
            print(f"{n:5d} {time_naive:15.4f} {time_memo:15.4f} {time_tab:15.4f} {ratio_str:>15}")
        else:
            print(f"{n:5d} {'TIMEOUT':>15} {time_memo:15.4f} {time_tab:15.4f} {'N/A':>15}")
    
    print()
    
    # Verify all solutions are identical
    print("=" * 80)
    print("SOLUTION VERIFICATION (Revenue must match)")
    print("=" * 80)
    
    all_match = True
    for r in results:
        if r['rev_naive'] is not None:
            match = r['rev_naive'] == r['rev_memo'] == r['rev_tab']
            status = "MATCH" if match else "MISMATCH"
            if not match:
                all_match = False
            print(f"n={r['n']}: Naive={r['rev_naive']}, Memo={r['rev_memo']}, Tab={r['rev_tab']} [{status}]")
        else:
            print(f"n={r['n']}: Naive=TIMEOUT, Memo={r['rev_memo']}, Tab={r['rev_tab']}")
    
    print()
    if all_match:
        print("All solutions produce identical results: VERIFIED")
    print()


# =============================================================================
# ANALYSIS
# =============================================================================
def print_analysis():
    print("=" * 80)
    print("ANALYSIS: Why Solutions Differ")
    print("=" * 80)
    print()
    
    print("1. NAIVE RECURSIVE: O(2^n) calls")
    print("   - Recalculates same subproblems repeatedly")
    print("   - Example: cut(5) calls cut(4), cut(3), cut(2), cut(1)")
    print("   - Then cut(4) calls cut(3), cut(2), cut(1) again (redundant)")
    print("   - Total calls: exponential in n")
    print()
    
    print("2. TOP-DOWN MEMOIZED: O(n^2) calls")
    print("   - Stores results in memo table")
    print("   - Each subproblem solved only once")
    print("   - Call count = n + sum of recursive calls to unique subproblems")
    print("   - For each n, tries all cuts 1..n (n iterations per size)")
    print("   - Total work: O(n^2)")
    print()
    
    print("3. BOTTOM-UP TABULATED: O(n^2) operations (no recursion)")
    print("   - Iterates through sizes 1..n (n iterations)")
    print("   - For each size i, tries all cuts 1..i")
    print("   - Total operations: 1+2+3+...+n = O(n^2)")
    print("   - No recursion overhead, pure loops")
    print()
    
    print("4. PERFORMANCE COMPARISON")
    print("   Naive:      2^n calls")
    print("   Memo/Tab:   n^2 operations")
    print("   Speedup:    Exponential! For n=25: 2^25 vs 25^2 = 33M vs 625")
    print()
    
    print("5. CALL REDUCTION")
    print("   Naive calls are cumulative sums of all subproblems solved multiple times")
    print("   Memoized eliminates redundant computation by caching")
    print("   Speedup grows exponentially with n")
    print()


# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    print_results_small()
    benchmark()
    print_analysis()
    print("=" * 80)
    print("TESTING COMPLETE")
    print("=" * 80)
