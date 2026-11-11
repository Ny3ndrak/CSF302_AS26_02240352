import heapq
import time
import random
from typing import Dict, List, Tuple, Optional, Set

# =============================================================================
# 1. DIJKSTRA'S ALGORITHM (Binary Heap)
# =============================================================================
def dijkstra(graph: Dict[str, List[Tuple[str, int]]], source: str) -> Tuple[Dict[str, int], Dict[str, Optional[str]]]:
    """
    Dijkstra's algorithm: shortest paths from source to all vertices.
    Time: O((V + E) log V) with binary heap
    
    graph: adjacency list {vertex: [(neighbor, weight), ...]}
    Returns: (distances, parents)
    """
    distances = {vertex: float('inf') for vertex in graph}
    distances[source] = 0
    parents = {vertex: None for vertex in graph}
    
    pq = [(0, source)]  # (distance, vertex)
    visited = set()
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        # Skip if we've already found a better path
        if current_dist > distances[current]:
            continue
        
        # Check neighbors
        for neighbor, weight in graph[current]:
            new_dist = distances[current] + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                parents[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))
    
    return distances, parents


def print_shortest_paths(distances: Dict[str, int], parents: Dict[str, Optional[str]], source: str):
    """Print shortest paths in readable format."""
    print(f"Shortest paths from source '{source}':")
    print(f"{'Vertex':>10} {'Distance':>12} {'Path':>30}")
    print("-" * 55)
    
    for vertex in sorted(distances.keys()):
        dist = distances[vertex]
        dist_str = str(dist) if dist != float('inf') else "INF"
        
        # Reconstruct path
        path = []
        current = vertex
        while current is not None:
            path.append(current)
            current = parents[current]
        path.reverse()
        
        path_str = " -> ".join(path) if dist != float('inf') else "No path"
        print(f"{vertex:>10} {dist_str:>12} {path_str:>30}")
    
    print()


# =============================================================================
# UNION-FIND (FOR KRUSKAL'S ALGORITHM)
# =============================================================================
class UnionFind:
    """Union-find data structure for cycle detection."""
    def __init__(self, vertices: List[str]):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}
    
    def find(self, x: str) -> str:
        """Find root with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x: str, y: str) -> bool:
        """Union by rank. Returns True if successful (no cycle)."""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Cycle detected
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        return True


# =============================================================================
# 2. KRUSKAL'S ALGORITHM
# =============================================================================
def kruskal(vertices: List[str], edges: List[Tuple[str, str, int]]) -> Tuple[List[Tuple[str, str, int]], int]:
    """
    Kruskal's algorithm: MST using union-find.
    Time: O(E log E) for sorting + O(E * α(V)) for union-find ≈ O(E log E)
    
    Returns: (MST edges, total weight)
    """
    # Sort edges by weight
    sorted_edges = sorted(edges, key=lambda x: x[2])
    
    uf = UnionFind(vertices)
    mst_edges = []
    total_weight = 0
    
    for u, v, weight in sorted_edges:
        if uf.union(u, v):
            mst_edges.append((u, v, weight))
            total_weight += weight
            
            if len(mst_edges) == len(vertices) - 1:
                break
    
    return mst_edges, total_weight


# =============================================================================
# 3. PRIM'S ALGORITHM
# =============================================================================
def prim(graph: Dict[str, List[Tuple[str, int]]], start: str) -> Tuple[List[Tuple[str, str, int]], int]:
    """
    Prim's algorithm: MST using binary heap.
    Time: O((V + E) log V) with binary heap
    
    Returns: (MST edges, total weight)
    """
    visited = set()
    mst_edges = []
    total_weight = 0
    
    # Heap of (weight, vertex, parent)
    pq = [(0, start, None)]
    
    while pq:
        weight, v, parent = heapq.heappop(pq)
        
        if v in visited:
            continue
        
        visited.add(v)
        
        if parent is not None:
            mst_edges.append((parent, v, weight))
            total_weight += weight
        
        # Add neighbors to heap
        for neighbor, edge_weight in graph[v]:
            if neighbor not in visited:
                heapq.heappush(pq, (edge_weight, neighbor, v))
    
    return mst_edges, total_weight


# =============================================================================
# GRAPH GENERATION
# =============================================================================
def generate_random_graph(num_vertices: int, num_edges: int) -> Tuple[List[str], List[Tuple[str, str, int]]]:
    """Generate random connected graph."""
    vertices = [f"v{i}" for i in range(num_vertices)]
    edges = set()
    
    # Ensure connectivity with spanning tree
    for i in range(num_vertices - 1):
        edges.add((vertices[i], vertices[i + 1], random.randint(1, 100)))
    
    # Add random edges until we have num_edges
    while len(edges) < num_edges:
        u = random.choice(vertices)
        v = random.choice(vertices)
        if u != v:
            weight = random.randint(1, 100)
            edges.add((u, v, weight))
    
    return vertices, list(edges)[:num_edges]


def graph_from_edges(vertices: List[str], edges: List[Tuple[str, str, int]]) -> Dict[str, List[Tuple[str, int]]]:
    """Convert edge list to adjacency list (undirected)."""
    graph = {v: [] for v in vertices}
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))
    return graph


# =============================================================================
# MAIN TESTING
# =============================================================================
def main():
    print("=" * 80)
    print("SHORTEST PATHS AND MINIMUM SPANNING TREES")
    print("=" * 80)
    print()
    
    # =========================================================================
    # 1. DIJKSTRA'S ALGORITHM - EXAMPLE
    # =========================================================================
    print("PART 1: DIJKSTRA'S ALGORITHM")
    print("=" * 80)
    
    graph_dijkstra = {
        'A': [('B', 7), ('C', 9), ('F', 14)],
        'B': [('A', 7), ('C', 10), ('D', 15)],
        'C': [('A', 9), ('B', 10), ('D', 11), ('F', 2)],
        'D': [('B', 15), ('C', 11), ('E', 6)],
        'E': [('D', 6), ('F', 9)],
        'F': [('A', 14), ('C', 2), ('E', 9)],
    }
    
    print("Graph edges:")
    for u in sorted(graph_dijkstra.keys()):
        for v, w in graph_dijkstra[u]:
            if u < v:
                print(f"  {u}-{v}: {w}")
    print()
    
    distances, parents = dijkstra(graph_dijkstra, 'A')
    print_shortest_paths(distances, parents, 'A')
    
    # =========================================================================
    # 2. KRUSKAL VS PRIM - EXAMPLE
    # =========================================================================
    print("PART 2: KRUSKAL AND PRIM ALGORITHMS")
    print("=" * 80)
    
    vertices_small = ['A', 'B', 'C', 'D', 'E', 'F']
    edges_small = [
        ('A', 'B', 7), ('A', 'C', 9), ('A', 'F', 14),
        ('B', 'C', 10), ('B', 'D', 15),
        ('C', 'D', 11), ('C', 'F', 2),
        ('D', 'E', 6),
        ('E', 'F', 9),
    ]
    
    print("Graph edges:")
    for u, v, w in sorted(edges_small):
        print(f"  {u}-{v}: {w}")
    print()
    
    # Kruskal
    kruskal_edges, kruskal_weight = kruskal(vertices_small, edges_small)
    print(f"Kruskal's MST (weight = {kruskal_weight}):")
    for u, v, w in sorted(kruskal_edges):
        print(f"  {u}-{v}: {w}")
    print()
    
    # Prim
    graph_prim = graph_from_edges(vertices_small, edges_small)
    prim_edges, prim_weight = prim(graph_prim, 'A')
    print(f"Prim's MST (weight = {prim_weight}):")
    for u, v, w in prim_edges:
        print(f"  {u}-{v}: {w}")
    print()
    
    print(f"Kruskal and Prim give same weight: {kruskal_weight == prim_weight}")
    print()
    
    # =========================================================================
    # 3. VERIFY ON RANDOM GRAPHS
    # =========================================================================
    print("PART 3: VERIFICATION ON RANDOM GRAPHS")
    print("=" * 80)
    print()
    print(f"{'Trial':>6} {'Vertices':>10} {'Edges':>10} {'Kruskal':>12} {'Prim':>12} {'Match':>8}")
    print("-" * 60)
    
    all_match = True
    for trial in range(10):
        num_vertices = random.randint(5, 20)
        num_edges = random.randint(num_vertices, min(30, num_vertices * (num_vertices - 1) // 2))
        
        vertices, edges = generate_random_graph(num_vertices, num_edges)
        
        kruskal_edges, kruskal_weight = kruskal(vertices, edges)
        graph = graph_from_edges(vertices, edges)
        prim_edges, prim_weight = prim(graph, vertices[0])
        
        match = "YES" if kruskal_weight == prim_weight else "NO"
        if kruskal_weight != prim_weight:
            all_match = False
        
        print(f"{trial:6d} {num_vertices:10d} {num_edges:10d} {kruskal_weight:12d} {prim_weight:12d} {match:>8}")
    
    print()
    print(f"All tests match: {all_match}")
    print()
    
    # =========================================================================
    # 4. TIMING COMPARISON
    # =========================================================================
    print("PART 4: TIMING COMPARISON (V=1000)")
    print("=" * 80)
    print()
    
    num_vertices = 1000
    
    # Sparse graph: E ~ 3V
    num_edges_sparse = 3 * num_vertices
    print(f"Sparse graph: V={num_vertices}, E={num_edges_sparse} (E ~ 3V)")
    vertices_sparse, edges_sparse = generate_random_graph(num_vertices, num_edges_sparse)
    
    start = time.time()
    k_edges, k_weight = kruskal(vertices_sparse, edges_sparse)
    time_kruskal_sparse = (time.time() - start) * 1000
    
    graph_sparse = graph_from_edges(vertices_sparse, edges_sparse)
    start = time.time()
    p_edges, p_weight = prim(graph_sparse, vertices_sparse[0])
    time_prim_sparse = (time.time() - start) * 1000
    
    print(f"  Kruskal: {time_kruskal_sparse:.2f} ms (weight={k_weight})")
    print(f"  Prim:    {time_prim_sparse:.2f} ms (weight={p_weight})")
    print(f"  Winner:  {'Prim' if time_prim_sparse < time_kruskal_sparse else 'Kruskal'}")
    print()
    
    # Dense graph: E ~ V²/4
    num_edges_dense = num_vertices * num_vertices // 4
    print(f"Dense graph: V={num_vertices}, E={num_edges_dense} (E ~ V²/4)")
    vertices_dense, edges_dense = generate_random_graph(num_vertices, num_edges_dense)
    
    start = time.time()
    k_edges, k_weight = kruskal(vertices_dense, edges_dense)
    time_kruskal_dense = (time.time() - start) * 1000
    
    graph_dense = graph_from_edges(vertices_dense, edges_dense)
    start = time.time()
    p_edges, p_weight = prim(graph_dense, vertices_dense[0])
    time_prim_dense = (time.time() - start) * 1000
    
    print(f"  Kruskal: {time_kruskal_dense:.2f} ms (weight={k_weight})")
    print(f"  Prim:    {time_prim_dense:.2f} ms (weight={p_weight})")
    print(f"  Winner:  {'Prim' if time_prim_dense < time_kruskal_dense else 'Kruskal'}")
    print()
    
    # =========================================================================
    # 5. DIJKSTRA WITH NEGATIVE EDGE
    # =========================================================================
    print("PART 5: DIJKSTRA FAILS WITH NEGATIVE EDGES")
    print("=" * 80)
    print()
    
    print("Graph with a negative-weight cycle:")
    graph_negative = {
        'A': [('B', 1)],
        'B': [('A', 1), ('C', 2), ('D', 100)],
        'C': [('B', 2), ('D', -10)],
        'D': [('B', 100), ('C', -10), ('E', 5)],
        'E': [('D', 5)],
    }
    
    print("Edges:")
    for u in sorted(graph_negative.keys()):
        for v, w in graph_negative[u]:
            if u < v or (u > v and w < 0):
                print(f"  {u}-{v}: {w}")
    print()
    
    print("Correct shortest path A to E:")
    print("  A -> B -> C -> D -> E: 1 + 2 + (-10) + 5 = -2")
    print()
    
    distances, parents = dijkstra(graph_negative, 'A')
    print("Dijkstra result:")
    print(f"  Distance A to E: {distances['E']}")
    print()
    
    print("Why Dijkstra fails with negative edges:")
    print("  - Assumes all edge weights are non-negative")
    print("  - Once a vertex is visited, distance is final")
    print("  - Negative edges can provide better paths after a vertex is visited")
    print("  - With negative cycles, no finite shortest path exists")
    print("  - Bellman-Ford algorithm correctly detects negative cycles")
    print()
    
    # =========================================================================
    # ANALYSIS
    # =========================================================================
    print("=" * 80)
    print("ANALYSIS")
    print("=" * 80)
    print()
    
    print("1. DIJKSTRA'S ALGORITHM")
    print("   Time: O((V + E) log V) with binary heap")
    print("   Space: O(V)")
    print("   Requires: Non-negative edge weights")
    print()
    
    print("2. KRUSKAL'S ALGORITHM")
    print("   Time: O(E log E) for sorting + O(E * inverse_ackermann(V)) for union-find")
    print("   Space: O(V + E)")
    print("   Better for sparse graphs (E << V*V)")
    print()
    
    print("3. PRIM'S ALGORITHM")
    print("   Time: O((V + E) log V) with binary heap")
    print("   Space: O(V + E)")
    print("   Better for dense graphs (E ~ V*V)")
    print()
    
    print("4. SPARSE VS DENSE")
    print(f"   Sparse (E={num_edges_sparse}): Kruskal {time_kruskal_sparse:.2f}ms vs Prim {time_prim_sparse:.2f}ms")
    print(f"   Dense (E={num_edges_dense}):  Kruskal {time_kruskal_dense:.2f}ms vs Prim {time_prim_dense:.2f}ms")
    print()


if __name__ == "__main__":
    main()
