from color_blocks_state import color_blocks_state, init_goal_for_search 

# --- Global Data ---
goal_state = []
index_map = {}       # Maps value -> list of indices [i1, i2...]
neighbors_map = {}   # Maps value -> sorted list of neighbor values
goal_adjacent_color_pairs = set() # Optimized set for O(1) heuristic lookups

def init_goal_for_heuristics(goal_blocks):
    global goal_state, index_map, neighbors_map, goal_adjacent_color_pairs
    
    # 1. Parse Goal String
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

    # 2. Build index_map (value -> LIST of indices)
    index_map = {}
    for i, v in enumerate(goal_state):
        if v not in index_map:
            index_map[v] = []
        index_map[v].append(i)

    # 3. Build neighbors_map (value -> sorted list of neighbors)
    neighbors_map = {}
    for i, v in enumerate(goal_state):
        neigh = []
        if i > 0:
            neigh.append(goal_state[i - 1])
        if i < len(goal_state) - 1:
            neigh.append(goal_state[i + 1])
        neighbors_map[v] = sorted(neigh)

    # 4. Build optimized pairs set for base_heuristic
    # We sort the pair (min, max) so lookups are order-independent
    pairs = set()
    for i in range(len(goal_state) - 1):
        left, right = goal_state[i], goal_state[i+1]
        if left <= right:
            pairs.add((left, right))
        else:
            pairs.add((right, left))
    goal_adjacent_color_pairs = pairs

def base_heuristic(_color_blocks_state):
    """
    Optimized Base Heuristic.
    Instead of scanning the goal_state list (O(N*M)), this uses O(1) set lookups.
    Complexity: O(N) where N is the number of blocks in the current state.
    """
    blocks = _color_blocks_state.getBlocks()
    heu = 0
    
    # Iterate through adjacent blocks in the current state
    for i in range(len(blocks) - 1):
        currTupA = blocks[i]
        currTupB = blocks[i+1]
        
        found_connection = False
        
        # Check if ANY color in Block A is adjacent to ANY color in Block B in the goal
        # We use the pre-calculated goal_adjacent_color_pairs set.
        for colorA in currTupA:
            for colorB in currTupB:
                # Create a canonical sorted pair to match the set keys
                pair = (colorA, colorB) if colorA <= colorB else (colorB, colorA)
                
                if pair in goal_adjacent_color_pairs:
                    found_connection = True
                    break
            if found_connection:
                break
        
        # If these two blocks are NOT neighbors in the goal, add a penalty
        if not found_connection:
            heu += 1
            
    return heu 

def advanced_heuristic(state):
    """
    Advanced heuristic checking index distances.
    Optimized with early exits and clearer logic.
    """
    blocks = state.getBlocks()
    h = 0
    
    if not blocks:
        return 0

    # --- Case 1: First block's left color check ---
    # The very first color of the first block must exist in the goal
    first_left = blocks[0][0]
    found_first_left = first_left in index_map
    if not found_first_left:
        h += 1

    # --- Iterate through adjacent blocks ---
    for i in range(len(blocks) - 1):
        A = blocks[i]
        B = blocks[i + 1]
        
        # Check if the "Left" side of the next block is valid in goal map
        # (Assuming block structure is consistent)
        if B[0] not in index_map:
            h += 1

        # --- Case 3: Adjacency Logic using specific Indices ---
        pair_ok = False

        # Nested loop optimization:
        # We only need to find ONE valid connection between the two blocks
        # to consider them "connected" in this heuristic step.
        for cA in A:
            if cA not in index_map: continue
            
            # Get list of goal indices for color A
            indices_A = index_map[cA]

            for cB in B:
                if cB not in index_map: continue
                
                # Get list of goal indices for color B
                indices_B = index_map[cB]
                
                # Check absolute distance between indices
                # Since lists are usually short, nested iteration is okay here,
                # but we break immediately upon finding a match.
                for idxA in indices_A:
                    for idxB in indices_B:
                        if abs(idxA - idxB) == 1:
                            pair_ok = True
                            break
                    if pair_ok: break
                if pair_ok: break
            if pair_ok: break

        if not pair_ok:
            h += 1

    return h