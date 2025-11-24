import os
import time

import psutil
from heuristics import *
from color_blocks_state import *
from search import *

if __name__ == '__main__':

    start_blocks = "(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(13,14)"
    goal_blocks = "4,14,6,2,8,12,10"
    init_goal_for_heuristics(goal_blocks)
    init_goal_for_search(goal_blocks)
    start_state = color_blocks_state(start_blocks)
    start_time = time.time()
    search_result = search(start_state, base_heuristic)
    end_time = time.time() - start_time
    
    # runtime
    print(end_time)
    # solution cost
    # 
    # {5:(4),3:(2),6:(1,7)}
    # {4:(5),2:(3),1:(6),7:(6)}
    # 
    print((search_result))
    print("-----------------")
    for node in search_result:
        print(node.state.get_state_str())
        print("-----",node.g)
        
    process = psutil.Process(os.getpid())
    mem_bytes = process.memory_info().rss   # memory in bytes

    mem_mib = mem_bytes / (1024 ** 2)
    print(f"Memory Used: {mem_mib:.2f} MiB")    
    print(search_result[-1].g)