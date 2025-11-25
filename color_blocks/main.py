import os
import time

import psutil
from heuristics import *
from color_blocks_state import *
from search import *

if __name__ == '__main__':

    start_blocks = "(4,12),(5,6),(8,2),(5,4),(3,5),(5,12),(9,7),(1,12)"
    goal_blocks = "3,5,1,4,5,8,7,12"
    init_goal_for_heuristics(goal_blocks)
    init_goal_for_search(goal_blocks)
    start_state = color_blocks_state(start_blocks)
    start_time = time.time()
    search_result = search(start_state, advanced_heuristic )
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