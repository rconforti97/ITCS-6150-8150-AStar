import numpy as np
from copy import copy, deepcopy
import queue

class Node:
    def __init__(self, value, parent, h, g):
        self.value = value # our current board
        self.parent = parent # the parent board
        self.h = h  # heuristic cost
        self.g = g  # the depth cost 
        self.f = h+g  # path and heuristic

    def __lt__(self, other):
        if self.f < other.f:
            return True
        else:
            return False

#######################################################################################
# This takes the boards from the board file and reads them in. 
def getBoards(filename):
    board = []
    with open(filename) as f:
        for l in f.readlines():
            board.append([int(x) for x in l.split(',')])
    f.close()
    print('Boards from boards.txt file:\n%s' % board, '\n')
    return board

# This takes the boards from boards.txt file and turns them into matrixs
def boardsToMatrix(boards):
    matrix_board = []
    for i in boards:
        temp_boards = np.array(i)
        matrix_board.append(np.reshape(temp_boards, (3,3), order='C'))
    return matrix_board

# Get the inversion count
def getInvCount(board) :
    inv_count = 0
    for i in range(0, len(board)):
        for j in range(i + 1, len(board)):
            if board[i] > board[j] and board[j] != 0:
                inv_count += 1
    return inv_count
     
# Returns True is solveable False if not
def isSolvable(boards) : 
    invCount = getInvCount(boards)
    return (invCount % 2 == 0)

def printSolveableBoards(boards):
    temp_boards = []
    for i in boards:
        placeholder = i
        if(isSolvable(placeholder)) :
            print("Board", placeholder, "Solvable")
            temp_boards += deepcopy([i])
        else:
            print("Board", i, "NOT Solvable")

    print('\nBoards we will be solving %s' % temp_boards)
    return temp_boards

def setPath(current, path, openList):
    while current.parent != '': # so this is why 4 isnt printing since its the goal board it has no parent
        path.insert(0, current.parent.value)
        current = current.parent
    if len(openList) == 1:
        path.insert(0, current.value)
        
def printPath(path):
    print("Start")
    for c in path: 
        for x in c:
            for n in x: 
                print(n, end=" ")
            print("")
        print("")

#######################################################################################
# I am just doing number of misplaced tiles as a heuritstic 
def heuristic(startNode, goalNode):
    temp_value = 0
    for i in range(0, 3):
        for j in range(0, 3):
            start_x, start_y = np.where(startNode == startNode[i][j])
            goal_x, goal_y = np.where(goalNode == startNode[i][j])
            temp_value += (abs(start_x - goal_x) + abs(start_y - goal_y))
            
            # if startNode[i][j] != goalNode[i][j] and startNode[i][j] != 0:
            #     temp_value += 1
    return temp_value

# -------------------
# | 0,0 | 0,1 | 0,2 |
# | 1,0 | 1,1 | 1,2 |
# | 2,0 | 2,1 | 2,2 |
# -------------------

def getNeighbors(board):
    x, y = np.where(board == 0) # getting the index of zero
    
    # print('\nboards in board', board)
    x = int(x)
    y = int(y)
    
    # print(x,y)
    neighbors = []
    
    # up to be in bounds have to be larger then -1 (x value)
    up_temp = x
    up_temp -= 1 
    if up_temp > -1:
        # print('up')
        temp_board_up = board.copy()
        temp_spot_up = temp_board_up[x-1][y]
        temp_board_up[x-1][y] = temp_board_up[x][y]
        temp_board_up[x][y] = temp_spot_up
        neighbors.append(temp_board_up)
        
    # right to be in bounds have to be less then 3 (y value)
    right_temp = y
    right_temp += 1
    if right_temp < 3 and right_temp > 0 and y != 2:
        # print('right')
        temp_board_right = board.copy()
        temp_spot_right = temp_board_right[x][y+1]
        temp_board_right[x][y+1] = temp_board_right[x][y]
        temp_board_right[x][y] = temp_spot_right
        neighbors.append(temp_board_right)

    # down to be in bounds have to be less then 3 (x value)
    down_temp = x
    down_temp += 1 
    if down_temp < 3 and x != 2:
        # print('down')
        temp_board_down = board.copy()
        temp_spot_down = temp_board_down[x+1][y]
        temp_board_down[x+1][y] = temp_board_down[x][y]
        temp_board_down[x][y] = temp_spot_down
        neighbors.append(temp_board_down)

    # left to be in bounds have to be more then -1 (y value)
    left_temp = y
    left_temp -= 1
    if left_temp < 3 and left_temp > -1:
        temp_board_left = board.copy()
        temp_spot_left = temp_board_left[x][y-1]
        temp_board_left[x][y-1] = temp_board_left[x][y]
        temp_board_left[x][y] = temp_spot_left
        neighbors.append(temp_board_left)
        
    neighbors = np.array(neighbors)
    # print('neighbors\n', neighbors)
    return neighbors



def inList(board, passed_list):
    print('**************************')
    # print('board\n', board.value)
    for i in passed_list:
        # print('i\n', i.value, '\n')
        if np.array_equal(i.value, board.value) == True:
            print('found a matching board')
            return True
    print('no matching board ')
    return False

def expandNode(node, openList, openListCopy, closedList, goal):
    children = getNeighbors(node.value)
    for c in children:
        child_g = 1 + node.g
        nd = Node(c, node, heuristic(c, goal), child_g) # value, parent, h, g
        
        if nd.h == 0:  # This is due to board 3 
            openList.put(nd)
            openListCopy.append(nd)
            break
        
        # print('closed/open list check')
        if not inList(nd, closedList) and not inList(nd, openListCopy):
            print('entered if in EN')
            openList.put(nd)
            openListCopy.append(nd)
        
        elif inList(nd, openListCopy):
            print('entered elif in EN')
            print('nd.g | node.g', nd.g, node.g)
            if nd.g < node.g:
                print('i got past the child g node check')
                openList.put(nd)
                openList.remove(node)
                openListCopy.append(nd)
                openListCopy.remove(node)

def aStar(start, goal):
    current = Node(start, '', heuristic(start, goal), 0)
    path = []
    openList = queue.PriorityQueue() 
    openListCopy = [] 
    openList.put(current) 
    openListCopy.append(current) 
    closedList = []
    numExpanded = 0

    print(start)
    # test = 0 
    # while test < 1000:
    while current.h != 0:
        # test += 1
        current = openList.get()
        openListCopy.append(current)
        closedList.append(current)
        
        print('current\n', current.value, 'current.h', current.h)
        # input("")
        expandNode(current, openList, openListCopy, closedList, goal)
        numExpanded += 1
        openListCopy.sort(key = lambda node: node.f, reverse=False)
        
        print('Number of states expanded:', numExpanded)
        
    path.append(current.value) # showin it actualy finds goal
    setPath(current, path, openListCopy)
    printPath(path)
    print('Path cost:', current.g)
    print('Number of states expanded:', numExpanded)
    

# ---------------------------------------------------------------------------------------------
def main():
    # Getting boards ready for A* algo
    boards = getBoards('boards.txt')
    boards = printSolveableBoards(boards) 
    boards = boardsToMatrix(boards)
    
    goal = [[1, 2, 3],[4, 5, 6],[7, 8, 0]]
    
    aStar(boards[5], goal)
# 
if __name__ == '__main__':
    main()
    print('\nExiting normally. Thank you')
    
# =============================================================================
# Why wont board 5, 6, 7 work?
#      they are looping for some reason 
#      idk why its doing this. 
# So, I think its passing boards 0-4 because its not relying on the on the 
# search function to figure it out. However, boards 5, 6, 7 are and its always 
# returning false no matter what. I am not sure why this is happneing 
# =============================================================================

# old expand node 
# print('node.value', node.value)
# children = getNeighbors(node.value)
# for c in children:
#     child_g = 1 + node.g
#     nd = Node(c, node, heuristic(c, goal), child_g) # value, parent, h, g
 # print('inList Result:', inList(nd, openListCopy))
   # if inList(nd, openListCopy):
   #     # print('I am in here')
   #     new_g = nd.g
   #     old_g = node.g
   #     if new_g < old_g:
   #         # print('I am in new_g < old_g')
   #         openList.put(nd)
   #         openList.pop(node)
   #         openListCopy.append(nd)
   #         openListCopy.remove(node)
   #         if inList(nd, closedList):
   #             print("i am in inList(nd, closedList)")
   #             closedList.remove(node)
             
   # elif not inList(nd, closedList):
   #     # print("i am in not inList(nd, closedList)")
   #     openList.put(nd)
   #     openListCopy.append(nd)