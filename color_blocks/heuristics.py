from color_blocks_state import color_blocks_state, init_goal_for_search 


# you can add helper functions and params
goal_state = []

def init_goal_for_heuristics(goal_blocks):
    currNumber = ""
    global goal_state 
    goal_state = []
    counter = 0
    for c in goal_blocks:
        # print(c,'to add on ', currNumber, 'and we are on the last index ', goal_blocks.index(c),' and the length is ', len(goal_blocks))
        if counter == len(goal_blocks) - 1:
            # print('we are on the last character', c , '-to add on ', currNumber)
            currNumber += c
            goal_state.append(int(currNumber))
            continue
        if c==','  :
            goal_state.append(int(currNumber))
            currNumber = ""
        else:
            currNumber += c
        counter += 1
    
    
    
def base_heuristic(state):
    blocks = state.getBlocks()

    # --- צור סט של כל זוגות הצבעים מה-goal ---
    goal_pairs = set()

    for i in range(len(goal_state) - 1):
        a = goal_state[i]
        b = goal_state[i + 1]
        goal_pairs.add(tuple(sorted((a, b))))

    h = 0

    # עבור כל שני בלוקים צמודים במצב הנוכחי
    for i in range(len(blocks) - 1):
        block_a = blocks[i]
        block_b = blocks[i + 1]

        found = False

        # נבדוק אם יש קומבינציה חוקית
        for color_a in block_a:
            for color_b in block_b:
                if tuple(sorted((color_a, color_b))) in goal_pairs:
                    found = True
                    break
            if found:
                break

        if not found:
            h += 1

    return h

    
    
    

def advanced_heuristic(_color_blocks_state):
    return base_heuristic(_color_blocks_state)

