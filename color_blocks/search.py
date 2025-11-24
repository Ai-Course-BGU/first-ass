from heuristics import base_heuristic
from search_node import search_node
from color_blocks_state import color_blocks_state

import heapq

def create_open_set():
    return []     # heap will be a list

def create_closed_set():
    return {}     # dictionary: state_string -> node


def add_to_open(vn, open_set):
    heapq.heappush(open_set, vn)


def open_not_empty(open_set):
    return len(open_set) > 0


def get_best(open_set):
    return heapq.heappop(open_set)  # return vn, not (f, vn)


def add_to_closed(vn, closed_set):
    closed_set[vn.state.get_state_str()] = vn


# Helper to compare g values
def duplicate_in_open(vn, open_set):
    state_str = vn.state.get_state_str()
    
    isExist = False
    isGsmallerOrEqual = False
    if state_str in open_set:
        isExist = True
    else :
        return False
        
    old_node = open_set[state_str]
    print('old g:', old_node.g, 'new g:', vn.g)
    if vn.g > old_node.g or vn.g == old_node.g:
        isGsmallerOrEqual = True

    return isExist and isGsmallerOrEqual


def duplicate_in_closed(vn, closed_set):
    state_str = vn.state.get_state_str()
    isExist = False
    isGsmallerOrEqual = False
    if state_str in closed_set:
        isExist = True
    else :
        return False
        
    old_node = closed_set[state_str]
    print('old g:', old_node.g, 'new g:', vn.g)
    if vn.g > old_node.g or vn.g == old_node.g:
        isGsmallerOrEqual = True

    return isExist and isGsmallerOrEqual


# helps to debug sometimes..
def print_path(path):
    for i in range(len(path)-1):
        print(f"[{path[i].state.get_state_str()}]", end=", ")
    print(path[-1].state.state_str)


def search(start_state, heuristic):

    open_set = create_open_set()
    closed_set = create_closed_set()
    start_node = search_node(start_state, 0, heuristic(start_state))
    add_to_open(start_node, open_set)

    while open_not_empty(open_set):

        current = get_best(open_set)
        
        if current is None:
            break
        print ("best current node:", current.state.get_state_str(), "g:", current.g, "h:", current.h, "f:", current.f)
        if color_blocks_state.is_goal_state(current.state):
            path = []
            while current:
                path.append(current)
                current = current.prev
            path.reverse()
            return path

        add_to_closed(current, closed_set)

        for neighbor, edge_cost in current.get_neighbors():
            # print("edge cost:", edge_cost, "from", current.state.get_state_str(), "to", neighbor.get_state_str())
            curr_neighbor = search_node(neighbor, current.g + edge_cost,base_heuristic(neighbor), current)
            if not duplicate_in_open(curr_neighbor, open_set) and not duplicate_in_closed(curr_neighbor, closed_set):
                # print("adding to open:", curr_neighbor.state.get_state_str(), "g:", curr_neighbor.g, "h:", curr_neighbor.h, "f:", curr_neighbor.f)
                add_to_open(curr_neighbor, open_set)

    return None




