
goal_state = []
def init_goal_for_search(goal_blocks):
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
    for goal in goal_state:
        # pass
        print('goal state after init:', goal)

class color_blocks_state:
    # you can add global params
    
    def __init__(self, blocks_str, **kwargs):
        # you can use the init function for several purposes
        self.blocks = []
        currNum = ""
        currTuple = ()
        for c in blocks_str:
            if c == ',' and currNum:
                currTuple += (int(currNum),)
                currNum = ""
                continue
            if c=='(' :
                currNum = ""
                currTuple = ()
                continue
            if c==')' :
                currTuple += (int(currNum),)
                currNum = ""
                self.blocks.append(currTuple)
                currTuple = ()
                continue
            currNum += c
        

    @staticmethod
    def is_goal_state(_color_blocks_state):
        # print('goal_state:', goal_state)
        for i in range(len(goal_state)):
            # print(_color_blocks_state.blocks[i][0], ',', goal_state[i])
            if _color_blocks_state.blocks[i][0] != goal_state[i]:
                return False
        return True
    
    def get_neighbors(self):
        neighbors = []
        for i in range (len(self.blocks)):
            new_state_flip = self.flip_block(i)
            if i!= len(self.blocks):
                neighbors.append((new_state_flip,1))
        for i in range (len(self.blocks)):
            new_state_spin = self.spin_block(i)
            neighbors.append((new_state_spin,0))
        return neighbors 
    # you can change the body of the function if you want
    # def __hash__(self):
    # you can change the body of the function if you want
    # def __eq__(self, other):
    # you can change the body of the function if you want

    # for debugging states
    def get_state_str(self):
        res = ""
        for b in self.blocks:
            res += "("
            for i in range(len(b)):
                res += str(b[i])
                if i != len(b) - 1:
                    res += ","
            res += ")"
            if b != self.blocks[-1]:
                res += ","
        return res

    def setBlocks(self, new_blocks):
        self.blocks = new_blocks

    #you can add helper functions [(1,2)]
    def flip_block(self, block_idx):
        copy_blocks = self.blocks.copy()
        currIndex = len(copy_blocks)-1
        while currIndex > block_idx:
            currTupple = copy_blocks[currIndex]
            copy_blocks[currIndex] = copy_blocks[block_idx]
            copy_blocks[block_idx] = currTupple
            currIndex -= 1
            block_idx += 1
        toRet = color_blocks_state("")
        toRet.setBlocks(copy_blocks)
        return toRet
        
            
    def spin_block(self, block_idx):
        copy_blocks = self.blocks.copy()
        copy_blocks[block_idx] = tuple(reversed(copy_blocks[block_idx]))
        toRet = color_blocks_state("")
        toRet.setBlocks(copy_blocks)
        return toRet
    def getBlockAt(self, index):
        return self.blocks[index]
    def getBlocks(self):
        return self.blocks
    
# stam = color_blocks_state("(5,2),(1,3),(9,22),(21,4)")
# init_goal_for_search("2,22,4,3")
# print(color_blocks_state.is_goal_state(stam))
# init_goal_for_search("5,1,9,21")
# print(color_blocks_state.is_goal_state(stam))
# for state in goal_state:
#     print(state,'\n')
# stam.spin_block(0)
# print(stam.blocks[0])
# stam.flip_block(2)
# print(stam.blocks)
# neighbors = stam.get_neighbors()
# print('neighbors:')
# for neighbor in neighbors:
#     print(neighbor)