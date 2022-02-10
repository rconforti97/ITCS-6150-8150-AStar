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
    while current.parent != '':
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
        print('  \u2193')

#######################################################################################
# I am just doing number of misplaced tiles as a heuritstic 
def heuristic(startNode, goalNode):
    temp_value = 0
    for i in range(0, 3):
        for j in range(0, 3):
            start_x, start_y = np.where(startNode == startNode[i][j])
            goal_x, goal_y = np.where(goalNode == startNode[i][j])
            temp_value += (abs(start_x - goal_x) + abs(start_y - goal_y))
    return temp_value


def getNeighbors(board):
    x, y = np.where(board == 0)
    x = int(x)
    y = int(y)
    
    neighbors = []
    
    # up to be in bounds have to be larger then -1 (x value)
    up_temp = x
    up_temp -= 1 
    if up_temp > -1:
        temp_board_up = board.copy()
        temp_spot_up = temp_board_up[x-1][y]
        temp_board_up[x-1][y] = temp_board_up[x][y]
        temp_board_up[x][y] = temp_spot_up
        neighbors.append(temp_board_up)
        
    # right to be in bounds have to be less then 3 (y value)
    right_temp = y
    right_temp += 1
    if right_temp < 3 and right_temp > 0 and y != 2:
        temp_board_right = board.copy()
        temp_spot_right = temp_board_right[x][y+1]
        temp_board_right[x][y+1] = temp_board_right[x][y]
        temp_board_right[x][y] = temp_spot_right
        neighbors.append(temp_board_right)

    # down to be in bounds have to be less then 3 (x value)
    down_temp = x
    down_temp += 1 
    if down_temp < 3 and x != 2:
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
    return neighbors



def inList(board, passed_list):
    for i in passed_list:
        if np.array_equal(i.value, board.value) == True:
            return True
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
        
        if not inList(nd, closedList) == True and not inList(nd, openListCopy) == True:
            openList.put(nd)
            openListCopy.append(nd)
        
        elif inList(nd, openListCopy):
            if nd.g < node.g:
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

    # print(start)
    while current.h != 0:
        current = openList.get()
        openListCopy.append(current)
        closedList.append(current)
        
        expandNode(current, openList, openListCopy, closedList, goal)
        numExpanded += 1
        
        if numExpanded and numExpanded % 100 == 0:
            print('Expanding nodes - one moment please')
        
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
    
    for i in boards:
        print("\n****************************\nHit enter to solve board:\n", i)
        input("")
        aStar(i, goal)
    # aStar(boards[6], goal)
# 
if __name__ == '__main__':
    main()
    print('\nExiting normally. Thank you')