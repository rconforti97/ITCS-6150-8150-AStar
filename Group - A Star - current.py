import numpy as np
from copy import copy, deepcopy

# import sys
################################################################
# Where I left off - 
#



# Questions
# Do we need to remove unsolveable boards? If so, create list and pass that list 
# in
################################################################
# Create a Node struct.
class Node:
    def __init__(self, value, parent, g, h):
        self.value = value 
        self.parent = parent
        self.f = g + h # 
        self.g = g # path for A*
        self.h = h # heruistic for A* 
        
        
# This takes the boards from the board file and reads them in. 
def getBoards(filename):
    board = []
    with open(filename) as f:
        for l in f.readlines():
            board.append([int(x) for x in l.split(',')])
    f.close()
    return board

# This takes the boards from boards.txt file and turns them into matrixs
def boardsToMatrix(boards):
    matrix_board = []
    for i in boards:
        temp_boards = np.array(i)
#        print('\n temp_board', temp_boards)
        matrix_board.append(np.reshape(temp_boards, (3,3), order='C'))
    boards = matrix_board.copy()
    return boards


def getInvCount(arr):
    inv_count = 0
    empty_value = -1
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if arr[j] != empty_value and arr[i] != empty_value and arr[i] > arr[j]:
                inv_count += 1
    return inv_count


def isSolvable(puzzle) :
    # Count inversions in given 8 puzzle
    inv_count = getInvCount([j for sub in puzzle for j in sub])
    # return true if inversion count is even.
    return (inv_count % 2 == 0)


def heuristic(currentloc, goal):
    # change to manhatten distance 
    return abs(currentloc[0] - goal[0]) + abs(currentloc[1] - goal[1])
    

# =============================================================================
# # assuming location is the blank space 
#     # assuming grid is a 2-day array. index [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
#     # -------------------
#     # | 0,0 | 0,1 | 0,2 |
#     # | 1,0 | 1,1 | 1,2 |
#     # | 2,0 | 2,1 | 2,2 |
#     # -------------------
# =============================================================================
def getNeighbors(board):
    x1, x2 = np.where(board == 0) # getting the index of zero
    
    # I was puting [[0]][[0]] instead of [0][0] so passing as a int 
    x1 = int(x1)
    x2 = int(x2)
    
    
    # print('x1:', x1, 'x2:', x2, ' inside GN')
    # print('passed in board \n:', board)
    
    neighbors = [] # to hold all the neighboring states
    
    # up to be in bounds have to be larger then -1 (x value)
    up_temp = x1
    up_temp -= 1 # by subtracting one we can we if it would be out of bounds of the 3,3 grid
    if up_temp > -1:
        # swap [x1, y1] with [x2, y2]
        temp_board_up = board.copy() # to copy the board
        
        temp_spot = temp_board_up[x1-1][x2]
        temp_board_up[x1-1][x2] = temp_board_up[x1][x2]
        temp_board_up[x1][x2] = temp_spot
        
        # return the whole grid
        neighbors.append(temp_board_up)
        # print('up move\n', temp_board_up)

    # right to be in bounds have to be less then 3 (y value)
    right_temp = x2
    right_temp += 1
    if right_temp < 3 and right_temp > 0:
        temp_board_right = board.copy() # to copy the board
        
        temp_spot = temp_board_right[x1][x2+1]
        temp_board_right[x1][x2+1] = temp_board_right[x1][x2]
        temp_board_right[x1][x2] = temp_spot
        
        # return the whole grid
        neighbors.append(temp_board_right)
        # print('right move\n', temp_board_right)

    # down to be in bounds have to be less then 3 (x value)
    down_temp = x1
    down_temp += 1 
    if down_temp < 3:
        temp_board_down = board.copy()
        
        temp_spot = temp_board_down[x1+1][x2]
        temp_board_down[x1+1][x2] = temp_board_down[x1][x2]
        temp_board_down[x1][x2] = temp_spot
        
        # return the whole grid
        neighbors.append(temp_board_down)
        # print('down move\n', temp_board_down)

    # left to be in bounds have to be more then -1 (y value)
    left_temp = x2
    left_temp += 1
    if left_temp < 3 and left_temp > 0:
        temp_board_left = board.copy() # to copy the board
        
        temp_spot = temp_board_left[x1][x2-1]
        temp_board_left[x1][x2-1] = temp_board_left[x1][x2]
        temp_board_left[x1][x2] = temp_spot
        
        # return the whole grid
        neighbors.append(temp_board_left)
        # print('left move\n', temp_board_left)
        
    
    print('neightbors return \n', neighbors)
    return neighbors

openList = []
closedList = []

# Create a function or method called expandNode that will do the following.
def expandNode(node):
    neighbors = getNeighbors(node)
    openedNeighbors = [] # The list of opened node neighbors
    closedNeighbors = [] # The list of closed node neighbors
    
    for i in neighbors:
        if(i.value in openList):
            openedNeighbors.append(i)
        if(i.value in closedList):
            closedNeighbors.append(i)

    return

def main():
    # Step 1 - Read in Boards 
    boards = getBoards('boards.txt') # reading in the boards 
    print('Boards from file: %s' % boards) # printing ou the boards
    
    # Step 2 - Figure out if solveable
    solveable_boards = []
    for i in boards:
        puzzle = [i]
        if(isSolvable(puzzle)):
            print("Board ", i, "  is Solvable")
            solveable_boards += deepcopy([i]) # deepcopy b/c without this it was copying as a 3-d array 
        else :
            print("Board ", i, "  is NOT Solvable")
    
    print('\nNew list of solveable boards: ', solveable_boards)
    
    # Print solveable boards to matrix 
    boards = boardsToMatrix(solveable_boards) # creating the matrix boards to a new variable 
    print('Boards turned to matrix \n', boards) # prining out the matrix boards
    
    # getNeighbors(new_boards[2])
    
    
if __name__ == "__main__":
   main()