import heapq
from heuristics import base_heuristic
from search_node import search_node
from color_blocks_state import color_blocks_state

# -----------------------------
# Optimized Open/Closed Sets
# -----------------------------
def create_open_set():
    """Return an empty open set (heap, dict)."""
    return [], {}  # heap, dict

def create_closed_set():
    """Return an empty closed set (dict)."""
    return {}  # state -> search_node

def add_to_open(node, open_set):
    """Add a node to the open set (heap + dict)."""
    open_heap, open_dict = open_set
    heapq.heappush(open_heap, node)
    open_dict[node.state] = node

def open_not_empty(open_set):
    open_heap, _ = open_set
    return len(open_heap) > 0

def get_best(open_set):
    """Pop the best node (lowest f) from the heap that is still in open_dict."""
    open_heap, open_dict = open_set
    while open_heap:
        node = heapq.heappop(open_heap)
        if node.state in open_dict and open_dict[node.state] is node:
            del open_dict[node.state]
            return node
    return None

def add_to_closed(node, closed_set):
    closed_set[node.state] = node

def duplicate_in_open(node, open_set):
    """Check if a better node already exists in open set."""
    _, open_dict = open_set
    existing = open_dict.get(node.state)
    if existing is None:
        return False
    if existing.g <= node.g:
        return True
    else:
        open_dict[node.state] = node
        return False

def duplicate_in_closed(node, closed_set):
    """Check if a better node already exists in closed set."""
    existing = closed_set.get(node.state)
    if existing is None:
        return False
    if existing.g <= node.g:
        return True
    else:
        del closed_set[node.state]
        return False

# -----------------------------
# Optimized A* Search
# -----------------------------
def search(start_state, heuristic, debug=False):
    """
    Optimized A* search using:
      - open set: (heap, dict)
      - closed set: dict
    """
    open_set = create_open_set()
    closed_set = create_closed_set()

    start_node = search_node(start_state, 0, heuristic(start_state))
    add_to_open(start_node, open_set)

    while open_not_empty(open_set):
        current = get_best(open_set)
        if current is None:
            break

        # if debug:
        # print(f"BEST: {current.state.get_state_str()}, g={current.g}, h={current.h}, f={current.f}")
        # print(f"Open size: {len(open_set[0])}, Closed size: {len(closed_set)}")

        # Goal check
        if color_blocks_state.is_goal_state(current.state):
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = node.prev
            path.reverse()
            return path

        add_to_closed(current, closed_set)

        # Expand neighbors
        for neighbor_state, cost in current.get_neighbors():
            new_g = current.g + cost
            new_node = search_node(neighbor_state, new_g, heuristic(neighbor_state), current)

            if duplicate_in_open(new_node, open_set):
                continue
            if duplicate_in_closed(new_node, closed_set):
                continue

            add_to_open(new_node, open_set)

    return None  # No solution found
