import numpy as np
from copy import copy, deepcopy
import queue

class Node:
    def __init__(self, value, parent, h, g):
        self.parent = parent # the parent board
        self.value = value # our current board
        self.g = g  # the depth cost 
        self.h = h  # heuristic cost
        self.f = g + h  # path and heuristic

    def __lt__(self, other):
        if self.g < other.g:
            return True
        else:
            return False
        # if self.f < other.f:
        #     return True
        # else:
        #     return False

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
            
    # print('heuristic value:', temp_value)
    return temp_value

 #         if startNode[i][j] != goalNode[i][j] and startNode[i][j] != 0:
 #             print('startNode[i][j]', startNode[i][j])
 #             print('goalNode[i][j]', goalNode[i][j])
 #             temp_value += 1

# -------------------
# | 0,0 | 0,1 | 0,2 |
# | 1,0 | 1,1 | 1,2 |
# | 2,0 | 2,1 | 2,2 |
# -------------------

def getNeighbors(board):
    x, y = np.where(board == 0) # getting the index of zero
    
    x = int(x)
    y = int(y)
    
    neighbors = []
    
    # up to be in bounds have to be larger then -1 (x value)
    up_temp = x
    up_temp -= 1 
    if up_temp > -1:
        # print('board line 95', board)
        temp_board_up = board.copy() # to copy the board
        # print('temp board up line 97', temp_board_up)
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
    # print('let_temp', left_temp)
    # if left_temp < 3 and left_temp > 0 and y != 0:
    if left_temp < 3 and left_temp > -1:
        temp_board_left = board.copy()
        temp_spot_left = temp_board_left[x][y-1]
        temp_board_left[x][y-1] = temp_board_left[x][y]
        temp_board_left[x][y] = temp_spot_left
        neighbors.append(temp_board_left)
        
    neighbors = np.array(neighbors)
    # print('neighbors', neighbors)
    return neighbors

def setPath(current, path, openList):
    while current.parent != '': # so this is why 4 isnt printing since its the goal board it has no parent
        path.insert(0, current.parent.value)
        current = current.parent
    if len(openList) == 1:
        path.insert(0, current.value)
        
def printPath(path):
    print("path")
    for c in path: 
        for x in c:
            for n in x: 
                print(n, end=" ")
            print("")
        print("")

# This is still wrong - comparative is incorrect. 
def inList(board, passed_list):
    for i in passed_list:
        # print(board)
        # print(i)
        # if (board.value == i.value).any():
        if board == i:
            return True
        else:
            return False

def expandNode(node, openList, openListCopy, closedList, goal):
    children = getNeighbors(node.value)
    for c in children:
        child_g = 1 + node.g
        nd = Node(c, node, heuristic(c, goal), child_g) # value, parent, h, g
        # print('nd h', nd.h)
        if nd.h == 0:  # This is due to board 3 
            openList.put(nd)
            openListCopy.append(nd)
            break
        # print('inList Result:', inList(nd, openListCopy))
        if inList(nd, openListCopy):
            # print('I am in here')
            new_g = nd.g
            old_g = node.g
            if new_g < old_g:
                # print('I am in new_g < old_g')
                openList.put(nd)
                openList.pop(node)
                openListCopy.append(nd)
                openListCopy.remove(node)
                if inList(nd, closedList):
                    print("i am in inList(nd, closedList)")
                    closedList.remove(node)
                    
        elif not inList(nd, closedList):
            # print("i am in not inList(nd, closedList)")
            openList.put(nd)
            openListCopy.append(nd)
            
        
        
        # if not inList(nd, closedList) and not inList(nd, openListCopy):
        #     openList.put(nd)
        #     openListCopy.append(nd)

def aStar(start, goal):
    print('\nStart', start)
    current = Node(start, '', heuristic(start, goal), 0)
    goal = goal
    path = []
    openList = queue.PriorityQueue() 
    openListCopy = [] 
    openList.put(current) 
    openListCopy.append(current) 
    closedList = []
    numExpanded = 0

    # test = 0 
    # while test <6:
    while True:
        # test += 1
        current = openList.get()
        closedList.append(current)
        
        
        # So we can get a bring out of the board as it goes
        # print("path")
        # for c in current.value: 
        #     for n in c: 
        #         print(n, end=" ")
        #     print("")

        if(current.h == 0):
            print('goal formation found')
            break

        else:
            # print('\n\ncurrent.value\n', current.value)
            expandNode(current, openList, openListCopy, closedList, goal)
            numExpanded += 1
            # print('numExpanded', numExpanded)
            
    print('current', current.value)
    if not openList.empty() or current.h == 0:
        setPath(current, path, openListCopy)
        
    if current.h != 0:
        print("Path NOT found - Failed!")
    
    return [path, numExpanded]

# ---------------------------------------------------------------------------------------------
def main():
    boards = getBoards('boards.txt')
    boards = printSolveableBoards(boards) 
    boards = boardsToMatrix(boards)
    goal = [[1, 2, 3],[4, 5, 6],[7, 8, 0]]
    # goal = np.reshape(goal, (3,3), order='C')
    
    
    # print('boards[0] type line 228', type(boards[5]))
    # print(boards[5])
    # boards[0].tolist()
    
    # getNeighbors(boards[2])

    [path, numExpanded] = aStar(boards[5], goal)
    print('Number of states expanded: %d' % numExpanded)
    printPath(path)

if __name__ == '__main__':
    main()
    print('\nExiting normally. Thank you')
    
# =============================================================================
# Why wont board 5, 6, 7 work?
#      they are looping for some reason 
#      idk why its doing this. 
# =============================================================================
