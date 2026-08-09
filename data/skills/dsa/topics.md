<!-- Topics for Data Structures & Algorithms. Format reference: MASTER.md → "File formats". -->

## Complexity analysis
- id: complexity-analysis
- status: strong
- priority: 1
- min_required: true
- focus: false
- updated: 2026-06-15

### What "enough" looks like
- Can state time and space complexity of your own solution without prompting
- Can identify the bottleneck and say what the next-better complexity class would require
- Comfortable with amortised analysis (dynamic array growth, union-find)

### Notes / log
- 2026-06-15: consistently getting this right unprompted in mock interviews

## Arrays, two pointers, sliding window
- id: arrays-two-pointers
- status: strong
- priority: 2
- min_required: true
- focus: false
- updated: 2026-06-22

### What "enough" looks like
- Recognises the pattern from the problem statement within a minute
- Can handle the fiddly variants: variable-size window, window with a counter map
- Gets the boundary conditions right first time

### Notes / log
- 2026-06-22: ~30 problems done, hit rate is high

## Hash maps and sets
- id: hash-maps-sets
- status: strong
- priority: 3
- min_required: true
- focus: false
- updated: 2026-06-22

### What "enough" looks like
- Default tool for lookup problems; reaches for it without thinking
- Can explain collision handling and why worst case is O(n)
- Knows when an ordered structure is required instead

### Notes / log
- 2026-06-22: solid

## Binary search
- id: binary-search
- status: comfortable
- priority: 4
- min_required: true
- focus: false
- updated: 2026-07-05

### What "enough" looks like
- Can write it without off-by-one errors, including lower/upper bound variants
- Recognises "binary search on the answer" problems
- Can prove the loop invariant if asked

### Notes / log
- 2026-07-05: still occasionally fumble the upper-bound variant under time pressure

## Trees and graph traversal
- id: trees-graphs
- status: comfortable
- priority: 5
- min_required: true
- focus: false
- updated: 2026-07-18

### What "enough" looks like
- BFS and DFS from memory, iterative and recursive
- Comfortable with topological sort, cycle detection, connected components
- Can pick the right traversal for the problem rather than defaulting to one

### Notes / log
- 2026-07-18: graph problems are fine; tree reconstruction problems are shakier

## Dynamic programming
- id: dynamic-programming
- status: learning
- priority: 6
- min_required: true
- focus: true
- updated: 2026-08-08

### What "enough" looks like
- Can define the state and recurrence out loud before writing any code
- Comfortable converting top-down memoisation to bottom-up, and doing the space optimisation
- Recognises the standard families: knapsack, LIS, edit distance, interval DP

### Notes / log
- 2026-08-03: worked through knapsack and LIS
- 2026-08-08: still slow at defining state on unfamiliar problems — this is the weak spot

## Heaps and priority queues
- id: heaps-priority-queues
- status: learning
- priority: 7
- min_required: false
- focus: false
- updated: 2026-07-25

### What "enough" looks like
- Recognises top-k and merge-k patterns immediately
- Knows the heapify complexity result and why it is O(n) not O(n log n)

### Notes / log
- 2026-07-25: done a handful; needs more reps

## Backtracking
- id: backtracking
- status: not-started
- priority: 8
- min_required: false
- focus: false

### What "enough" looks like
- Can write the standard template and prune it sensibly
- Comfortable with permutations, subsets, N-queens, word search

### Notes / log
- Not started.
