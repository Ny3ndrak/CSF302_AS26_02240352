# Lab 1 - Algorithm Performance Analysis
**Student Number:** 02240352  
**Course:** CSF302 | **Assignment:** AS26

---

## Question 1: Linear Search vs Binary Search
**File:** `Lab1_Q1_BinarySearch.py`

### Algorithm Implementation
- **Linear Search (_352):** O(n) complexity - scans array sequentially
- **Binary Search (_352):** O(log n) complexity - divides search space in half
- **Input Sizes:** 1,000 | 5,000 | 10,000 | 50,000 | 100,000 | 500,000 | 1,000,000
- **Trials:** 7 repetitions with 20 search targets per trial

### Output Screenshot
<!-- Insert Q1 terminal output screenshot here -->
![Q1 Output](screenshots/q1_output_352.png)

### CSV Results
Results saved to: `q1_results_352.csv`

---

## Question 2: Bubble Sort vs Merge Sort
**File:** `Lab1_Q2_SortComparison.py`

### Algorithm Implementation
- **Bubble Sort (_352):** O(n²) complexity - compares adjacent elements
- **Merge Sort (_352):** O(n log n) complexity - divide and conquer approach
- **Input Sizes:** 100 | 500 | 1,000 | 2,000 | 4,000 | 8,000
- **Trials:** Adaptive (15 trials for small arrays, 3 for large)

### Output Screenshot
<!-- Insert Q2 terminal output screenshot here -->
![Q2 Output](screenshots/q2_output_352.png)

### CSV Results
Results saved to: `q2_results_352.csv`

---

## Question 3: Prime Number Generation Comparison
**File:** `Lab1_Q3_PrimeGeneration.py`

### Algorithm Implementation
- **Naive Trial Division (_352):** O(n²) - checks all divisors up to n-1
- **Optimized Trial Division (_352):** O(n√n) - checks divisors up to √n
- **Sieve of Eratosthenes (_352):** O(n log log n) - most efficient
- **Input Sizes:** 10,000 | 50,000 | 100,000 | 500,000 | 1,000,000

### Output Screenshot
<!-- Insert Q3 terminal output screenshot here -->
![Q3 Output](screenshots/q3_output_352.png)

### CSV Results
Results saved to: `q3_results_352.csv`

---

## How to Run

```powershell
# Question 1
python Lab1_Q1_BinarySearch.py

# Question 2
python Lab1_Q2_SortComparison.py

# Question 3
python Lab1_Q3_PrimeGeneration.py
```

---

## Repository Structure

```
CSF302_AS26_02240352/
└── Lab1_AS26/
    ├── Lab1_Q1_BinarySearch.py
    ├── Lab1_Q2_SortComparison.py
    ├── Lab1_Q3_PrimeGeneration.py
    ├── lab_screenshot.md
    ├── q1_results_352.csv
    ├── q2_results_352.csv
    ├── q3_results_352.csv
    └── screenshots/
        ├── q1_output_352.png
        ├── q2_output_352.png
        └── q3_output_352.png
```

---

## Naming Convention Compliance

✅ **Repository:** CSF302_AS26_02240352  
✅ **Folder:** Lab1_AS26  
✅ **Files:** Lab1_Q<number>_<Description>.py  
✅ **Variables/Functions:** All use suffix `_352` (last 3 digits of student number)

### Example Functions:
- `linear_search_352()`, `binary_search_352()`
- `bubble_sort_352()`, `merge_sort_352()`
- `naive_primes_352()`, `optimized_primes_352()`, `sieve_of_eratosthenes_352()`
- All variables: `data_352`, `arr_352`, `n_352`, `i_352`, etc.

---

**Date:** August 10, 2026
