import random
from typing import List, Tuple, Dict, Optional

call_count = 0

# =============================================================================
# 1. BOTTOM-UP DP: Minimum Matrix Chain Multiplication
# =============================================================================
def matrix_chain_order_dp(p: List[int]) -> Tuple[List[List[int]], List[List[int]]]:
    """
    Bottom-up DP for matrix chain multiplication.
    p[i] = row count of matrix i, p[i+1] = column count of matrix i
    Matrix i has dimensions p[i] x p[i+1]
    
    Returns: (cost table m, split table s)
    m[i][j] = minimum cost to multiply matrices i..j
    s[i][j] = split index k for optimal solution
    """
    n = len(p) - 1  # Number of matrices
    
    # m[i][j] = min cost to multiply matrices i..j
    m = [[0] * n for _ in range(n)]
    
    # s[i][j] = split index k for optimal parenthesization
    s = [[0] * n for _ in range(n)]
    
    # l = chain length
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            m[i][j] = float('inf')
            
            # Try all split points k between i and j
            for k in range(i, j):
                # Cost of multiplying matrices i..k and k+1..j
                # Plus cost of multiplying the two results
                cost = m[i][k] + m[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k
    
    return m, s


def print_optimal_parens(s: List[List[int]], i: int, j: int) -> str:
    """Reconstruct optimal parenthesization."""
    if i == j:
        return f"A{i + 1}"
    else:
        k = s[i][j]
        left = print_optimal_parens(s, i, k)
        right = print_optimal_parens(s, k + 1, j)
        return f"({left}{right})"


# =============================================================================
# 2. BRUTE-FORCE RECURSIVE: Verify small instances
# =============================================================================
def matrix_chain_brute(p: List[int], i: int, j: int) -> Tuple[int, str]:
    """
    Brute-force recursive search for minimum matrix chain multiplication cost.
    Returns: (min_cost, optimal_parenthesization)
    """
    global call_count
    call_count += 1
    
    if i == j:
        return 0, f"A{i + 1}"
    
    min_cost = float('inf')
    best_parens = ""
    
    for k in range(i, j):
        cost_left, parens_left = matrix_chain_brute(p, i, k)
        cost_right, parens_right = matrix_chain_brute(p, k + 1, j)
        
        # Cost to multiply matrices i..k and k+1..j, then multiply results
        cost = cost_left + cost_right + p[i] * p[k + 1] * p[j + 1]
        
        if cost < min_cost:
            min_cost = cost
            best_parens = f"({parens_left}{parens_right})"
    
    return min_cost, best_parens


# =============================================================================
# 3. LEFT-TO-RIGHT ORDER: Baseline for comparison
# =============================================================================
def matrix_chain_leftright(p: List[int]) -> int:
    """Cost of multiplying matrices left-to-right: ((...((A1A2)A3)...)An)"""
    n = len(p) - 1
    cost = 0
    
    for i in range(n - 1):
        # Multiply matrices 0..i with matrix i+1
        # Dimensions: p[0] x p[i+1] times p[i+1] x p[i+2]
        # Result: p[0] x p[i+2]
        cost += p[0] * p[i + 1] * p[i + 2]
    
    return cost


# =============================================================================
# MAIN TESTING
# =============================================================================
def main():
    print("=" * 80)
    print("MATRIX CHAIN MULTIPLICATION ANALYSIS")
    print("=" * 80)
    print()
    
    # =========================================================================
    # TEST CASES
    # =========================================================================
    test_cases = [
        ("Test 1", [30, 35, 15, 5, 10, 20, 25]),
        ("Test 2", [5, 4, 6, 2, 7]),
    ]
    
    # Add 5 random chains
    for idx in range(5):
        n = random.randint(3, 8)
        dims = [random.randint(10, 100) for _ in range(n + 1)]
        test_cases.append((f"Random {idx + 1}", dims))
    
    # =========================================================================
    # RESULTS TABLE
    # =========================================================================
    print("BOTTOM-UP DP RESULTS")
    print("=" * 80)
    print()
    
    results = []
    
    for test_name, dims in test_cases:
        n = len(dims) - 1
        
        # Bottom-up DP
        m, s = matrix_chain_order_dp(dims)
        dp_cost = m[0][n - 1]
        dp_parens = print_optimal_parens(s, 0, n - 1)
        
        # Left-to-right baseline
        lr_cost = matrix_chain_leftright(dims)
        
        # Verify with brute-force (only if n <= 8)
        if n <= 8:
            global call_count
            call_count = 0
            bf_cost, bf_parens = matrix_chain_brute(dims, 0, n - 1)
            bf_calls = call_count
            
            match = "PASS" if dp_cost == bf_cost else "FAIL"
            print(f"{test_name} (n={n})")
            print(f"  DP Cost:       {dp_cost:12d}")
            print(f"  Brute Cost:    {bf_cost:12d} ({bf_calls:8d} calls) [{match}]")
            print(f"  Left-Right:    {lr_cost:12d} ({lr_cost/dp_cost:.2f}x)")
            print(f"  DP Parens:     {dp_parens}")
            print(f"  BF Parens:     {bf_parens}")
        else:
            print(f"{test_name} (n={n})")
            print(f"  DP Cost:       {dp_cost:12d}")
            print(f"  Left-Right:    {lr_cost:12d} ({lr_cost/dp_cost:.2f}x)")
            print(f"  DP Parens:     {dp_parens}")
            print(f"  (Brute-force skipped: n > 8)")
        
        print()
        results.append({
            'name': test_name,
            'n': n,
            'dims': dims,
            'dp_cost': dp_cost,
            'lr_cost': lr_cost,
            'dp_parens': dp_parens,
        })
    
    # =========================================================================
    # SUMMARY TABLE
    # =========================================================================
    print("=" * 80)
    print("SUMMARY: DP Cost vs Left-to-Right")
    print("=" * 80)
    print(f"{'Test':>20} {'n':>3} {'DP Cost':>15} {'Left-Right':>15} {'Savings':>12} {'Ratio':>8}")
    print("-" * 80)
    
    total_dp = 0
    total_lr = 0
    
    for r in results:
        savings = r['lr_cost'] - r['dp_cost']
        ratio = r['lr_cost'] / r['dp_cost'] if r['dp_cost'] > 0 else 0
        print(f"{r['name']:>20} {r['n']:3d} {r['dp_cost']:15d} {r['lr_cost']:15d} {savings:12d} {ratio:8.2f}x")
        total_dp += r['dp_cost']
        total_lr += r['lr_cost']
    
    print("-" * 80)
    savings_total = total_lr - total_dp
    ratio_total = total_lr / total_dp if total_dp > 0 else 0
    print(f"{'TOTAL':>20} {'-':3} {total_dp:15d} {total_lr:15d} {savings_total:12d} {ratio_total:8.2f}x")
    print()
    
    # =========================================================================
    # ANALYSIS
    # =========================================================================
    print("=" * 80)
    print("ANALYSIS")
    print("=" * 80)
    print()
    
    print("1. BOTTOM-UP DP ALGORITHM: O(n^3) time, O(n^2) space")
    print("   - Fills cost table m[i][j] for all chain lengths")
    print("   - For each subchain i..j, tries all split points k")
    print("   - Stores optimal split in s[i][j] for reconstruction")
    print()
    
    print("2. BRUTE-FORCE VERIFICATION: O(Catalan(n)) time")
    print("   - Recursively tries all possible parenthesizations")
    print("   - Catalan(n) = (2n)! / ((n+1)! * n!)")
    print("   - For n=5: 42 parenthesizations")
    print("   - For n=8: 1430 parenthesizations")
    print()
    
    print("3. LEFT-TO-RIGHT BASELINE")
    print("   - Multiplies left-to-right: ((...((A1 A2) A3) ...) An)")
    print("   - Often suboptimal; DP usually 2-10x better")
    print()
    
    print("4. KEY INSIGHT: Matrix dimensions matter greatly")
    print("   - Optimal split depends on relative sizes")
    print("   - Example: [30,35,15,5,10,20,25]")
    print("   - Grouping by similar-sized chunks reduces operations")
    print()


if __name__ == "__main__":
    main()
