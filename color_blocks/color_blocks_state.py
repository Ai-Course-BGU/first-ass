
goal_state = []
def init_goal_for_search(goal_blocks):
    currNumber = ""
    global goal_state
    goal_state=[]
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
            # if i!= len(self.blocks):
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
        # make a shallow copy of the list of tuples (safe!)
        copy_blocks = self.blocks.copy()

        # reverse everything from block_idx to the end
        copy_blocks[block_idx:] = reversed(copy_blocks[block_idx:])

        new_state = color_blocks_state("")
        new_state.setBlocks(copy_blocks)
        return new_state

    
    def spin_block(self, block_idx):
        copy_blocks = self.blocks.copy()

        copy_blocks[block_idx] = tuple(reversed(copy_blocks[block_idx]))

        new_state = color_blocks_state("")
        new_state.setBlocks(copy_blocks)
        return new_state

    def getBlockAt(self, index):
        return self.blocks[index]
    def getBlocks(self):
        return self.blocks
