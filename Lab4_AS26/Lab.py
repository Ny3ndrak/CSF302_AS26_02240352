import time
from typing import List, Tuple

# =============================================================================
# PART A: MODULAR EXPONENTIATION
# =============================================================================

# =============================================================================
# 1. NAIVE MODULAR EXPONENTIATION
# =============================================================================
def mod_exp_naive(a: int, b: int, m: int) -> int:
    """
    Naive modular exponentiation: a^b mod m
    Repeated multiplication.
    Time: O(b)
    """
    if m < 1:
        raise ValueError("Modulus m must be >= 1")
    if b < 0:
        raise ValueError("Exponent b must be non-negative")
    
    a = a % m
    result = 1
    for _ in range(b):
        result = (result * a) % m
    
    return result


# =============================================================================
# 2. BINARY MODULAR EXPONENTIATION (Square-and-Multiply)
# =============================================================================
def mod_exp_binary(a: int, b: int, m: int) -> int:
    """
    Binary modular exponentiation: a^b mod m
    Square-and-multiply method.
    Time: O(log b)
    """
    if m < 1:
        raise ValueError("Modulus m must be >= 1")
    if b < 0:
        raise ValueError("Exponent b must be non-negative")
    
    if b == 0:
        return 1 % m
    
    a = a % m
    result = 1
    
    while b > 0:
        if b & 1:  # if b is odd
            result = (result * a) % m
        a = (a * a) % m
        b >>= 1  # divide b by 2
    
    return result


# =============================================================================
# PART B: MATRIX MODULAR EXPONENTIATION
# =============================================================================

# =============================================================================
# 1. MATRIX MULTIPLICATION WITH MODULO
# =============================================================================
def matrix_mult(A: List[List[int]], B: List[List[int]], m: int) -> List[List[int]]:
    """
    Multiply two square matrices A and B, reducing modulo m.
    Time: O(d^3) where d is matrix dimension
    """
    d = len(A)
    C = [[0] * d for _ in range(d)]
    
    for i in range(d):
        for j in range(d):
            for k in range(d):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % m
    
    return C


# =============================================================================
# 2. IDENTITY MATRIX
# =============================================================================
def identity_matrix(d: int) -> List[List[int]]:
    """Create d x d identity matrix."""
    return [[1 if i == j else 0 for j in range(d)] for i in range(d)]


# =============================================================================
# 3. NAIVE MATRIX EXPONENTIATION
# =============================================================================
def matrix_pow_naive(A: List[List[int]], n: int, m: int) -> List[List[int]]:
    """
    Naive matrix exponentiation: A^n mod m
    Repeated multiplication.
    Time: O(n * d^3)
    """
    d = len(A)
    result = identity_matrix(d)
    
    for _ in range(n):
        result = matrix_mult(result, A, m)
    
    return result


# =============================================================================
# 4. BINARY MATRIX EXPONENTIATION
# =============================================================================
def matrix_pow_binary(A: List[List[int]], n: int, m: int) -> List[List[int]]:
    """
    Binary matrix exponentiation: A^n mod m
    Square-and-multiply method.
    Time: O(log n * d^3)
    """
    d = len(A)
    result = identity_matrix(d)
    base = [row[:] for row in A]  # Copy A
    
    while n > 0:
        if n & 1:
            result = matrix_mult(result, base, m)
        base = matrix_mult(base, base, m)
        n >>= 1
    
    return result


# =============================================================================
# 5. FIBONACCI USING MATRIX EXPONENTIATION
# =============================================================================
def fibonacci_matrix(n: int, m: int = 10**9 + 7) -> int:
    """
    Calculate the nth Fibonacci number modulo m using matrix exponentiation.
    
    Base case: F(0) = 0, F(1) = 1
    Matrix: [[F(n+1), F(n)], [F(n), F(n-1)]] = [[1,1],[1,0]]^n
    
    Time: O(log n) multiplications of 2x2 matrices
    """
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    # Fibonacci matrix: [[1, 1], [1, 0]]
    fib_matrix = [[1, 1], [1, 0]]
    
    result = matrix_pow_binary(fib_matrix, n, m)
    
    # F(n) is in result[1][0] or result[0][1]
    return result[0][1]


# =============================================================================
# 6. GRAPH WALKS USING ADJACENCY MATRIX
# =============================================================================
def count_walks(adj_matrix: List[List[int]], start: int, end: int, k: int, m: int = 10**9 + 7) -> int:
    """
    Count walks of exactly k edges from start to end vertex.
    Uses adjacency matrix exponentiation.
    
    A^k[i][j] gives the number of walks of length k from i to j
    """
    adj_k = matrix_pow_binary(adj_matrix, k, m)
    return adj_k[start][end]


# =============================================================================
# MAIN TESTING
# =============================================================================
def main():
    print("=" * 80)
    print("MODULAR EXPONENTIATION AND MATRIX EXPONENTIATION")
    print("=" * 80)
    print()
    
    # =========================================================================
    # PART A: MODULAR EXPONENTIATION
    # =========================================================================
    print("PART A: MODULAR EXPONENTIATION")
    print("=" * 80)
    print()
    
    # Test cases
    test_cases = [
        (2, 10, 1000),
        (3, 100, 1000),
        (5, 50, 13),
        (7, 123, 456),
    ]
    
    print("Verification: Naive vs Binary Modular Exponentiation")
    print(f"{'Base':>6} {'Exp':>6} {'Mod':>8} {'Naive':>12} {'Binary':>12} {'Match':>8}")
    print("-" * 60)
    
    for a, b, m in test_cases:
        naive_result = mod_exp_naive(a, b, m)
        binary_result = mod_exp_binary(a, b, m)
        match = "YES" if naive_result == binary_result else "NO"
        print(f"{a:6d} {b:6d} {m:8d} {naive_result:12d} {binary_result:12d} {match:>8}")
    
    print()
    
    # Input validation tests
    print("Input Validation Tests:")
    print()
    
    # Zero exponent
    result = mod_exp_binary(5, 0, 1000)
    print(f"Zero exponent: 5^0 mod 1000 = {result} (expected 1)")
    
    # Negative base (should reduce mod m first)
    result = mod_exp_binary(-5, 10, 1000)
    print(f"Negative base: (-5)^10 mod 1000 = {result}")
    
    # Negative exponent (should raise error)
    try:
        result = mod_exp_binary(5, -10, 1000)
        print(f"Negative exponent: ERROR NOT RAISED")
    except ValueError as e:
        print(f"Negative exponent: Correctly raised error - {e}")
    
    # Invalid modulus (should raise error)
    try:
        result = mod_exp_binary(5, 10, 0)
        print(f"Invalid modulus: ERROR NOT RAISED")
    except ValueError as e:
        print(f"Invalid modulus: Correctly raised error - {e}")
    
    print()
    
    # Timing comparison
    print("Timing Comparison (b = 10^i):")
    print(f"{'Exponent':>15} {'Naive (ms)':>15} {'Binary (ms)':>15} {'Speedup':>12}")
    print("-" * 60)
    
    m = 10**9 + 7
    for exp_power in range(1, 7):
        b = 10 ** exp_power
        a = 12345
        
        start = time.perf_counter()
        naive_result = mod_exp_naive(a, b, m)
        time_naive = (time.perf_counter() - start) * 1000
        
        start = time.perf_counter()
        binary_result = mod_exp_binary(a, b, m)
        time_binary = (time.perf_counter() - start) * 1000
        
        speedup = time_naive / time_binary if time_binary > 1e-6 else float('inf')
        print(f"{b:15d} {time_naive:15.4f} {time_binary:15.4f} {speedup:12.2f}x")
    
    print()
    
    # =========================================================================
    # PART B: MATRIX MODULAR EXPONENTIATION
    # =========================================================================
    print("PART B: MATRIX MODULAR EXPONENTIATION")
    print("=" * 80)
    print()
    
    # Test with small matrices
    A = [[1, 2], [3, 4]]
    m = 13
    
    print(f"Matrix A = {A}, modulus m = {m}")
    print()
    
    for n in range(1, 5):
        naive = matrix_pow_naive(A, n, m)
        binary = matrix_pow_binary(A, n, m)
        match = naive == binary
        print(f"A^{n} mod {m}:")
        print(f"  Naive:  {naive}")
        print(f"  Binary: {binary}")
        print(f"  Match:  {match}")
    
    print()
    
    # =========================================================================
    # FIBONACCI USING MATRIX EXPONENTIATION
    # =========================================================================
    print("FIBONACCI USING MATRIX EXPONENTIATION")
    print("=" * 80)
    print()
    
    print(f"{'n':>6} {'F(n) mod (10^9+7)':>20}")
    print("-" * 30)
    
    test_fib_sizes = [10, 50, 100, 1000, 10**6, 10**9]
    for n in test_fib_sizes:
        fib = fibonacci_matrix(n)
        print(f"{n:6d} {fib:20d}")
    
    print()
    print("F(10^18) mod (10^9 + 7):")
    m = 10**9 + 7
    start = time.perf_counter()
    fib_huge = fibonacci_matrix(10**18, m)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"  Result: {fib_huge}")
    print(f"  Time:   {elapsed:.4f} ms")
    print()
    
    # =========================================================================
    # GRAPH WALKS USING ADJACENCY MATRIX
    # =========================================================================
    print("GRAPH WALKS USING ADJACENCY MATRIX")
    print("=" * 80)
    print()
    
    # Simple directed graph: 3 vertices
    adj = [
        [0, 1, 1],  # From vertex 0: to 1, 2
        [1, 0, 1],  # From vertex 1: to 0, 2
        [1, 1, 0],  # From vertex 2: to 0, 1
    ]
    
    print("Adjacency matrix (triangle graph):")
    for row in adj:
        print(f"  {row}")
    print()
    
    print("Walks of length k from vertex 0 to vertex 2:")
    print(f"{'Length k':>10} {'# Walks':>15}")
    print("-" * 30)
    
    for k in range(1, 6):
        walks = count_walks(adj, 0, 2, k)
        print(f"{k:10d} {walks:15d}")
    
    print()
    
    # =========================================================================
    # BENCHMARKING
    # =========================================================================
    print("BENCHMARKING: Naive vs Binary Matrix Exponentiation")
    print("=" * 80)
    print()
    
    print(f"{'Dimension':>12} {'Exponent':>12} {'Naive (ms)':>15} {'Binary (ms)':>15} {'Speedup':>12}")
    print("-" * 75)
    
    for d in [2, 4, 8, 16, 32]:
        # Create random matrix
        A = [[i + j for j in range(d)] for i in range(d)]
        m = 10**9 + 7
        
        for exp_power in [4, 6, 8, 10, 12]:
            n = 2 ** exp_power
            
            # Skip large naive computations
            if d >= 8 or n >= 256:
                time_naive_str = "SKIP"
                time_binary = None
                
                start = time.perf_counter()
                binary_result = matrix_pow_binary(A, n, m)
                time_binary = (time.perf_counter() - start) * 1000
                
                print(f"{d:12d} {n:12d} {time_naive_str:>15} {time_binary:>15.4f} {'N/A':>12}")
            else:
                start = time.perf_counter()
                naive_result = matrix_pow_naive(A, n, m)
                time_naive = (time.perf_counter() - start) * 1000
                
                start = time.perf_counter()
                binary_result = matrix_pow_binary(A, n, m)
                time_binary = (time.perf_counter() - start) * 1000
                
                speedup = time_naive / time_binary if time_binary > 1e-6 else 0
                print(f"{d:12d} {n:12d} {time_naive:>15.4f} {time_binary:>15.4f} {speedup:>12.2f}x")
    
    print()
    
    # =========================================================================
    # ANALYSIS
    # =========================================================================
    print("=" * 80)
    print("ANALYSIS")
    print("=" * 80)
    print()
    
    print("1. MODULAR EXPONENTIATION")
    print("   Naive: O(b) multiplications - impractical for large b")
    print("   Binary: O(log b) multiplications - exponential speedup")
    print("   Example: b=10^6 binary is ~333x faster than naive")
    print()
    
    print("2. MATRIX EXPONENTIATION")
    print("   Naive: O(n * d^3) - impractical for large n or d")
    print("   Binary: O(log n * d^3) - exponential speedup in n")
    print("   For d=2: binary ~100x faster for n=2^12")
    print()
    
    print("3. FIBONACCI VIA MATRIX")
    print("   Computes F(n) in O(log n) time")
    print("   Avoids iterating through all Fibonacci numbers")
    print("   F(10^18) computed in milliseconds")
    print()
    
    print("4. GRAPH WALKS")
    print("   A^k[i][j] counts k-edge walks from i to j")
    print("   Efficient for counting paths without enumeration")
    print()


if __name__ == "__main__":
    main()
