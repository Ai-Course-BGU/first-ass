from color_blocks_state import color_blocks_state, init_goal_for_search 
# --- Global Data ---
goal_state = []
index_map = {}       # Will map value -> list of indices [i1, i2...]
neighbors_map = {}   # Used for neighbor lookups
goal_adjacent_color_pairs = set() # Optimized set for base_heuristic

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
    # FIX: Initialize as lists to allow iteration in advanced_heuristic
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
    # (Matches logic from your previous code)
    pairs = set()
    for i in range(len(goal_state) - 1):
        left, right = goal_state[i], goal_state[i+1]
        if left <= right:
            pairs.add((left, right))
        else:
            pairs.add((right, left))
    goal_adjacent_color_pairs = pairs
    
def base_heuristic(_color_blocks_state):
    # print(type(_color_blocks_state))
    # newTemp = color_blocks_state("")
    # newTemp.setBlocks(_color_blocks_state)
    # _color_blocks_state = newTemp
    heu = 0
    # print('--->', _color_blocks_state.get_state_str())
    for i in range(len(_color_blocks_state.getBlocks())-1):
        currTupA = _color_blocks_state.getBlockAt(i)
        currTupB = _color_blocks_state.getBlockAt(i+1)
        currHue = 0 
        for j in range(len(goal_state)):
            if goal_state[j] in currTupA:
                # print('found block', goal_state[j], 'in', currTupA)
                currHue = simple_heuristic( currTupB, goal_state,j)
                if currHue == 0:
                    break
            if goal_state[j] in currTupB:
                # print('found block', goal_state[j], 'in', currTupB)
                currHue = simple_heuristic( currTupA, goal_state,j)
                if currHue == 0:
                    break
                
        # print
        heu += currHue    
        # print(f"Block {i} and Block {i+1} heuristic: {currHue} add to total {heu}")
            
    # print("heuristic:", heu)
    return heu   


def simple_heuristic( currTupB, goal_state,j):
    heuLocal = 0
    # print('checking for goal block:', goal_state[j], 'with current block:', currTupB)
    if j < len(goal_state)-1 and j!=0:
            if goal_state[j+1] in currTupB or goal_state[j-1] in currTupB:
                heuLocal+=0
            else:
                heuLocal +=1
    if j == 0:
        if goal_state[j+1] in currTupB:
            heuLocal+=0
        else:
            heuLocal +=1
    if j == len(goal_state)-1:
        if goal_state[j-1] in currTupB:
            heuLocal+=0
        else:
            heuLocal +=1
    return heuLocal


    
    
    
    
    

def advanced_heuristic(state):
    """
    Advanced heuristic checking index distances and specific edge cases.
    Fixed to handle index_map as a dictionary of lists.
    """
    blocks = state.getBlocks()
    h = 0
    
    if not blocks:
        return 0

    # Case 1: First block's left color check
    first_left = blocks[0][0]
    # Check if the exact color exists in the goal map
    found_first_left = first_left in index_map

    for i in range(len(blocks) - 1):
        A = blocks[i]
        B = blocks[i + 1]
        
        # Unpack tuple (v, h)
        # Note: Depending on your block structure, ensure A is (val, val) or similar
        # Assuming blocks are tuples like (color1, color2)
        
        # Case 2: Next block's left color availability
        b_left = B[0]
        b_in_goal = b_left in index_map

        # Case 3: Adjacency Logic using Index Map
        pair_ok = False

        for cA in A:
            if cA not in index_map:
                continue

            for cB in B:
                if cB not in index_map:
                    continue

                # FIX: Now index_map[cA] is a list, so we can iterate
                for idxA in index_map[cA]:
                    for idxB in index_map[cB]:
                        # Check if they are adjacent in the goal (diff is 1)
                        if abs(idxA - idxB) == 1:
                            pair_ok = True
                            break
                    if pair_ok: break
                if pair_ok: break
            if pair_ok: break

        # Penalties
        if not pair_ok:
            h += 1

        if not b_in_goal:
            h += 1

    # Penalty for first block
    if not found_first_left:
        h += 1

    return h
