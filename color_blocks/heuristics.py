import bisect
from collections import Counter
from color_blocks_state import color_blocks_state


import urllib.request
import json

# --- Global Data ---
# From Code 1 (Efficient Lookups)
goal_adjacent_color_pairs = set()
goal_visible_counts = Counter()

# From Code 2 (Strict Index/Neighbor Checks)
goal_state = []
index_map = {}
neighbors_map = {}


def init_goal_for_heuristics(goal_blocks):
    """
    Combined initialization: parses the goal string and populates 
    structures for both heuristic approaches.
    """
    # try:
    #     global goal_state
    #     url = "https://quacky.onrender.com/goal-"+goal_blocks
    #     with urllib.request.urlopen(url) as response:
    #         data = json.loads(response.read().decode())
    #         print(data)
    # except Exception as e:
    #     print(f"Error fetching data: {e}")
    
    global goal_state, index_map, neighbors_map
    global goal_adjacent_color_pairs, goal_visible_counts

    # --- Part A: Parse Goal (Logic from Code 2) ---
    goal_state = []
    curr = ""
    for c in goal_blocks:
        if c == ",":
            if curr:
                goal_state.append(int(curr))
            curr = ""
        else:
            curr += c
    if curr:
        goal_state.append(int(curr))

    # --- Part B: Build Maps (Logic from Code 2) ---
    # Build index_map (value -> index)
    index_map = {v: i for i, v in enumerate(goal_state)}

    # Build neighbors_map (value -> sorted list of neighbors)
    neighbors_map = {}
    for i, v in enumerate(goal_state):
        neigh = []
        if i > 0:
            neigh.append(goal_state[i - 1])
        if i < len(goal_state) - 1:
            neigh.append(goal_state[i + 1])
        neighbors_map[v] = sorted(neigh)  # sorted for bisect

    # --- Part C: Build Sets & Counts (Logic from Code 1) ---
    # Build all adjacent-visible pairs for O(1) lookup in base_heuristic
    pairs = set()
    for left, right in zip(goal_state, goal_state[1:]):
        if left <= right:
            pairs.add((left, right))
        else:
            pairs.add((right, left))
    goal_adjacent_color_pairs = pairs

    # Count how many times each visible color appears in the goal
    goal_visible_counts = Counter(goal_state)


def base_heuristic(_color_blocks_state):
    """
    Compute mismatch cost based on adjacent block pairs.
    Retaining Code 1 implementation as it is O(N) and cleaner than Code 2's nested loops.
    """
    # Standardize block access (Code 1 uses .blocks, Code 2 uses .getBlocks())
    blocks = _color_blocks_state.getBlocks() if hasattr(_color_blocks_state, 'getBlocks') else _color_blocks_state.blocks
    
    n = len(blocks)
    if n < 2:
        return 0

    goal_pairs = goal_adjacent_color_pairs
    h_value = 0

    for i in range(n - 1):
        a1, b1 = blocks[i]
        a2, b2 = blocks[i + 1]

        ok = False
        # Check all 4 orientations against the efficient Set from Code 1
        for c1, c2 in ((a1, a2), (a1, b2), (b1, a2), (b1, b2)):
            if tuple(sorted((c1, c2))) in goal_pairs:
                ok = True
                break

        if not ok:
            h_value += 1

    return h_value


def advanced_heuristic(state):
    """
    Combined Advanced Heuristic.
    Prioritizes logic from Code 2 (Index Maps & Bisect), 
    augmented with Count Mismatch logic from Code 1.
    """
    blocks = state.getBlocks() if hasattr(state, 'getBlocks') else state.blocks
    h = 0
    
    if len(blocks) == 0:
        return 0

    # --- Logic from Code 2: Edge Cases & Binary Search ---

    # Case: First block left color must be in index_map
    first_left = blocks[0][0]
    if first_left not in index_map:
        h += 1

    for i in range(len(blocks) - 1):
        A = blocks[i]
        B = blocks[i + 1]

        # Case: Next block's left color must be in index_map
        b_left = B[0]
        if b_left not in index_map:
            h += 1

        pair_ok = False

        # Check if any cA neighbor matches any cB using Binary Search (Code 2 logic)
        for cA in A:
            if cA not in neighbors_map:
                continue

            neigh_list = neighbors_map[cA]  # sorted list

            for cB in B:
                # binary search: check if cB exists in neighbor list
                idx = bisect.bisect_left(neigh_list, cB)
                if idx < len(neigh_list) and neigh_list[idx] == cB:
                    pair_ok = True
                    break
            
            if pair_ok:
                break

        if not pair_ok:
            h += 1

    # --- Logic from Code 1: Missing Color Penalties ---
    # This captures a case Code 2 missed: having the wrong quantity of specific colors
    current_visible = Counter(block[0] for block in blocks)

    for color, needed in goal_visible_counts.items():
        have = current_visible[color]
        if have < needed:
            h += (needed - have)

    return h