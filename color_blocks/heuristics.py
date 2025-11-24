from color_blocks_state import color_blocks_state, init_goal_for_search 


# you can add helper functions and params
goal_state = []

def init_goal_for_heuristics(goal_blocks):
    currNumber = ""
    goal_state.clear()
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


    
    
    

def advanced_heuristic(_color_blocks_state):
    return 0

