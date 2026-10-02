# AI Use Disclosure

## Tools used
Deepseek was used as a conversational assistant throughout this
project. No code was submitted without being read, understood, and tested
locally.

## How it was used

### Conceptual explanation
For topics I found harder, I asked the assistant to explain the underlying
idea before writing any code:
- The distinction between tree search and graph search, and why the
  explored set is required for termination.
- The difference between a priority queue (ADT) and Python's `heapq`
  (implementation), and why decrease-key matters for A*.
- The admissibility and consistency conditions for heuristics, and why
  consistency allows skipping re-opening in A*.
- The MST lower bound for h3 and the dominance argument over h2.

These conversations shaped my mental model; the code was written by me
and checked against the explanations.

### Code review
After writing each method (environment, searches, heuristics), I pasted it
and asked for a review. In several cases the review caught bugs:
- Missing return paths in boolean helpers (`in_bounds`, `is_passable`)
  that would have returned `None` instead of `False`.
- A tuple-indexing error (`grid[r, c]` vs `grid[r][c]`).
- Missing `CLEAN` handling in an early draft of `get_actions`.

Each bug was explained conceptually, not just corrected — the review
identified why the bug occurred, not only what to type instead.

### Debugging
When a search returned wrong results or crashed, I described the symptom
and the assistant helped trace the cause. For example:
- `is_passable` throwing `TypeError` because it received a grid character
  instead of a position tuple.
- `h2` raising `ValueError` on an empty dirty set, fixed by an explicit
  guard.
- A* returning suboptimal paths, traced to checking the goal at push
  instead of at pop.

### What I did myself
- All code was typed and run locally.
- Every method was tested against the example grid before moving on.
- The heuristic admissibility arguments in the report were written in my
  own words after working through the reasoning with the assistant, and I
  can defend each one.
- The experiment runs and the analysis of the results are mine; the
  assistant helped structure the table and identify what the numbers show.

## What the assistant did not do
- It did not write the final versions of any method end-to-end without
  review on my part. Where code was provided directly (the A* and IDA*
  skeletons, the MST for h3), I read it, traced it on the example grid,
  and understand each line before including it.
- It did not generate the experiment data or the plots.
- It did not write the admissibility arguments verbatim; the report's
  wording is mine.