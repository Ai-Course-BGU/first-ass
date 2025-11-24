import heapq
from heuristics import base_heuristic
from search_node import search_node
from color_blocks_state import color_blocks_state


def create_open_set():
    return [], {}     # (heap, dict)


def create_closed_set():
    return {}         # dict only


def add_to_open(vn, open_heap, open_dict):
    heapq.heappush(open_heap, vn)
    open_dict[vn.state.get_state_str()] = vn


def open_not_empty(open_heap):
    return len(open_heap) > 0


def get_best(open_heap, open_dict):
    best = heapq.heappop(open_heap)
    state_str = best.state.get_state_str()
    
    # remove from dict
    if state_str in open_dict:
        del open_dict[state_str]

    return best


def add_to_closed(vn, closed_set):
    closed_set[vn.state.get_state_str()] = vn


def duplicate_in_open(vn, open_dict):
    state = vn.state.get_state_str()

    if state not in open_dict:
        return False

    old = open_dict[state]
    return vn.g >= old.g


def duplicate_in_closed(vn, closed_set):
    state = vn.state.get_state_str()

    if state not in closed_set:
        return False

    old = closed_set[state]
    return vn.g >= old.g


def search(start_state, heuristic):
    open_heap, open_dict = create_open_set()
    closed_set = create_closed_set()

    start_node = search_node(start_state, 0, heuristic(start_state))
    add_to_open(start_node, open_heap, open_dict)

    while open_not_empty(open_heap):

        current = get_best(open_heap, open_dict)

        
        
        print("BEST:", current.state.get_state_str(), 
              "g:", current.g, "h:", current.h, "f:", current.f)

        if color_blocks_state.is_goal_state(current.state):
            # reconstruct path
            path = []
            while current:
                path.append(current)
                current = current.prev
            return path[::-1]

        add_to_closed(current, closed_set)

        for neighbor, edge_cost in current.get_neighbors():
            new_g = current.g + edge_cost
            h = base_heuristic(neighbor)

            child = search_node(neighbor, new_g, h, current)

            if not duplicate_in_open(child, open_dict) \
               and not duplicate_in_closed(child, closed_set):

                add_to_open(child, open_heap, open_dict)

    return None
