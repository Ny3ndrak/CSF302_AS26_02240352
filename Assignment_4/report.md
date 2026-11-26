# Assignment 4: Booking the Hall

**AI use:** Copilot assisted with drafting the algorithms, tests, and analysis.
I checked the dynamic-programming result against exhaustive search on 500
seeded random cases and checked both greedy rules against optimal schedules.

## Counterexamples

Use the four requests below, where indices are shown in parentheses:

| Index | Start | Finish | Fee |
|---:|---:|---:|---:|
| 0 | 0 | 2 | 1 |
| 1 | 1 | 3 | 6 |
| 2 | 3 | 4 | 6 |
| 3 | 0 | 4 | 10 |

The optimal schedule is requests **1 and 2**, earning 12. Earliest-finish
greedy takes requests 0 and 2 for 7: it chooses the first-finishing request
even though that blocks the more valuable request 1. Highest-fee greedy takes
request 3 for 10, which blocks the compatible pair 1 and 2. Thus neither
greedy rule always maximizes revenue.

The assignment's example is also reproduced: earliest-finish earns 7,500
with requests `[0, 3, 4]`; the DP and highest-fee greedy earn 10,000 with
`[1, 4]`.

## Why the DP is correct

Sort requests by finish time. For request `j`, let `p(j)` be the number of
earlier requests whose finish time is no later than `j`'s start. Any optimal
schedule either excludes `j`, earning at most `OPT(j-1)`, or includes `j`.
When it includes `j`, all other selected requests must come from the compatible
prefix ending at `p(j)`, whose best revenue is `OPT(p(j))`. Therefore the
best revenue for the first `j` requests is
`OPT(j) = max(OPT(j-1), fee_j + OPT(p(j)))`. Reconstructing these choices
produces an optimal schedule. Equality at the boundary is allowed, so
back-to-back bookings are compatible.

## Greedy revenue on random inputs

For each of 1,000 seeded inputs, I generated 50 requests with integer start
times from 0 to 200, durations from 1 to 30, and fees from 1 to 1,000.
Revenue ratios are greedy revenue divided by the DP optimum.

| Rule | Average ratio | Worst ratio |
|---|---:|---:|
| Earliest finish | 80.34% | 43.09% |
| Highest fee | 90.18% | 60.03% |

On this sample, highest-fee greedy earned more on average, but neither rule
matched the optimum consistently. The ratio results depend on the input
distribution and are not guarantees for other booking data.

## Time complexity

Let `n` be the number of requests.

| Function | Time | Reason |
|---|---:|---|
| `greedy_earliest_finish` | `O(n log n)` | Sort by finish, then scan once |
| `greedy_highest_fee` | `O(n^2)` | Sort by fee; check each candidate against accepted requests |
| `best_schedule` | `O(n log n)` | Sort and binary-search predecessors; DP and reconstruction are linear |
| `brute_force` | `O(n 2^n)` | Examine up to `2^n` subsets, checking up to `n` requests each |

## Critical reflection

1. Testing can find counterexamples, but passing a finite test set cannot prove
   a greedy rule correct. The four-request example shows why: many ordinary
   cases can pass while a particular combination of overlaps and fees exposes
   the flaw. The DP recurrence and exhaustive checks provide stronger
   correctness evidence.
2. The manager should use the DP result when revenue matters. In my 1,000-case
   experiment, earliest-finish averaged 80.34% of optimal revenue and highest
   fee averaged 90.18%; their worst cases were 43.09% and 60.03%. A simple
   greedy rule may be reasonable only when speed or simplicity outweighs
   revenue loss.
3. When all fees are equal and non-negative, maximizing revenue is the same as
   maximizing the number of compatible bookings. Earliest-finish selection
   leaves as much room as possible for later bookings and is optimal for that
   unweighted objective. With different fees, maximizing the booking count is
   no longer the same as maximizing revenue.
