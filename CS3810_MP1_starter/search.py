"""
CS3810 Mini-Project 1 - Part 2: The Search Algorithms (100 points)
==================================================================

Implement dfs_search, astar_search, and idastar_search below. Do not change
the signatures or the return shapes: run_tests.py and the grading harness
unpack them exactly as documented.

You may NOT use a library implementation of DFS, A*, or IDA* (networkx,
simpleai, aima-python, ...). Using heapq, collections.deque, and the
provided PriorityQueue is expected and fine.

Metric definitions - use these, and say which you used in your report:

    nodes_expanded      A node is EXPANDED when it is removed from the
                        frontier and its successors are generated. Do not
                        count nodes that were merely generated.

    max_frontier_size   The largest number of live entries the frontier
                        ever held. For the PriorityQueue helper this is
                        len(queue), not len(queue.heap).

    iterations          (IDA* only) The number of depth-limited passes,
                        i.e. how many times the f-cost threshold was set.
                        A search that succeeds on the first threshold has
                        iterations == 1.

Suggested order of work: DFS first, then A*, then IDA*.
"""

import math

from priority_queue import PriorityQueue

# Sentinel used by the IDA* recursion to report success. Returning a plain
# number means "the smallest f-value I saw above the threshold".
FOUND = 'FOUND'


def dfs_search(problem):
    """
    Perform Depth-First Search.

    Args:
        problem: VacuumWorld instance

    Returns:
        Tuple (solution_path, nodes_expanded, max_frontier_size)
        solution_path: List of actions, or None if no solution
        nodes_expanded: Number of nodes expanded during search
        max_frontier_size: Maximum size of frontier during search

    Requirements:
        * Iterative, with an explicit stack. Do NOT recurse - you will hit
          Python's recursion limit on the larger grids.
        * Cycle detection with an explored set, or DFS will not terminate.
        * Returns the FIRST solution found. It will not be optimal, and it
          is not supposed to be.

    Hint: push (state, path_so_far) pairs. Push successors in reversed()
    order if you want the stack to explore them in ACTION_ORDER order.
    """
    
    start = problem.initial_state()
    stack = [(start, [])]         
    explored = set()
    nodes_expanded = 0
    max_frontier = 0              

    while stack:
        max_frontier = max(max_frontier, len(stack))
        state, path = stack.pop()

        if problem.is_goal(state):
            return (path, nodes_expanded, max_frontier)

        if state in explored:
            continue
        explored.add(state)
        nodes_expanded += 1

        for action in reversed(problem.get_actions(state)):   
            child = problem.result(state, action)
            if child not in explored:
                stack.append((child, path + [action]))

    return (None, nodes_expanded, max_frontier)
    #raise NotImplementedError("Part 2a: implement dfs_search")


def astar_search(problem, heuristic):
    """
    Perform A* Search.

    Args:
        problem: VacuumWorld instance
        heuristic: Function h(state, problem) -> estimated cost to goal

    Returns:
        Tuple (solution_path, nodes_expanded, max_frontier_size)

    Requirements:
        * Priority queue ordered by f(n) = g(n) + h(n).
        * Handle REOPENING: if you find a cheaper path to a state you have
          already expanded, you must be able to improve it. The provided
          PriorityQueue supports this - pushing an item already in the
          queue replaces its priority instead of duplicating it.
        * With an admissible heuristic this MUST return an optimal
          solution. run_tests.py checks that against known optimal costs.

    Hint: keep a dict g[state] of best-known cost-so-far and a dict
    came_from[state] = (parent_state, action) to rebuild the path at the
    end. A helper like _reconstruct() below keeps the main loop readable.
    """
    start = problem.initial_state()
    pq = PriorityQueue()
    h_start = heuristic(start, problem)
    pq.push(start, h_start)  

    best_g = {start: 0}
    came_from = {start: (None, None)} 
    explored = set()
    nodes_expanded = 0
    max_frontier = 1

    while pq:
        max_frontier = max(max_frontier, len(pq))
        state = pq.pop()

        if problem.is_goal(state):
            # reconstruct path
            path = []
            cur = state
            while came_from[cur][0] is not None:
                parent, action = came_from[cur]
                path.append(action)
                cur = parent
            path.reverse()
            return (path, nodes_expanded, max_frontier)

        explored.add(state)
        nodes_expanded += 1

        for action in problem.get_actions(state):
            child = problem.result(state, action)
            new_g = best_g[state] + problem.action_cost(state, action)

            if child in explored:
                # with consistent heuristic, skip
                continue

            if child not in best_g or new_g < best_g[child]:
                best_g[child] = new_g
                came_from[child] = (state, action)
                h = heuristic(child, problem)
                pq.push(child, new_g + h)

    return (None, nodes_expanded, max_frontier)
    #raise NotImplementedError("Part 2b: implement astar_search")


def _reconstruct(came_from, state):
    """Walk came_from backwards from `state` and return the action list.

    Args:
        came_from: Dict mapping state -> (parent_state, action)
        state: The goal state reached by the search

    Returns:
        List of actions from the initial state to `state`.
    """
    path = []
    
    while state in came_from:
        parent, action = came_from[state]
        if parent is None:
            break
        path.append(action)
        state = parent

    path.reverse()
    return path
    #raise NotImplementedError("Part 2b: implement _reconstruct (optional helper)")


def idastar_search(problem, heuristic):
    """
    Perform Iterative Deepening A* Search.

    Args:
        problem: VacuumWorld instance
        heuristic: Function h(state, problem) -> estimated cost to goal

    Returns:
        Tuple (solution_path, nodes_expanded, iterations)
        iterations: Number of depth-limited iterations performed

    Requirements:
        * Iterative deepening on an f-cost THRESHOLD, not on depth. The
          next threshold is the smallest f-value that exceeded the current
          one.
        * Linear space: no explored set carried across iterations. You may
          track the states on the current path to avoid immediate cycles.
        * Returns an optimal solution.

    Structure that works (write DFS and A* first - this will make far more
    sense once you have both):

        threshold = h(start)
        loop:
            result = search(start, g=0, threshold)
            if result is FOUND:    return the path
            if result is infinite: return None (no solution)
            threshold = result

    where search(state, g, threshold) returns FOUND, or the smallest
    f-value it saw that exceeded the threshold, or math.inf.
    """
    start = problem.initial_state()

    # Wrapped in a list so the nested search() can mutate it without nonlocal.
    stats = {'nodes': 0}
    iterations = 0

    def search(state, g, threshold, path_states):
        """Bounded DFS. Returns (True, path) or (False, next_threshold)."""
        f = g + heuristic(state, problem)
        if f > threshold:
            return (False, f)

        if problem.is_goal(state):
            return (True, [])

        stats['nodes'] += 1
        min_exceeded = float('inf')

        for action in problem.get_actions(state):
            child = problem.result(state, action)
            if child in path_states:
                continue

            path_states.add(child)
            new_g = g + problem.action_cost(state, action)
            found, val = search(child, new_g, threshold, path_states)
            path_states.remove(child)

            if found:
                return (True, [action] + val)
            if val < min_exceeded:
                min_exceeded = val

        return (False, min_exceeded)

    threshold = heuristic(start, problem)

    while True:
        iterations += 1
        path_states = {start}
        found, val = search(start, 0, threshold, path_states)

        if found:
            return (val, stats['nodes'], iterations)
        if val == float('inf'):
            return (None, stats['nodes'], iterations)
        threshold = val

    #raise NotImplementedError("Part 2c: implement idastar_search")


if __name__ == "__main__":
    # Quick manual check once you have implemented an algorithm:
    from test_grids import EXAMPLE, parse_grid
    from vacuum_world import VacuumWorld
    from heuristics import h2

    grid, start, dirty = parse_grid(EXAMPLE)
    problem = VacuumWorld(grid, start, dirty)

    path, expanded, frontier = astar_search(problem, h2)
    print("A* on the example grid (optimal cost is 14)")
    print("  cost     :", len(path) if path else None)
    print("  expanded :", expanded)
    print("  frontier :", frontier)
    print("  plan     :", path)
