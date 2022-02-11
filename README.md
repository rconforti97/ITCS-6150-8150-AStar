# ITCS-6150-8150-AStar
For ITCS 6150/8150 - Intelligent Systems course in 2022 Spring

# Algorithm:
I used the A Star algorithm

## Heuristic:
Using the manhatten distance I calculated the amount of moves it would take to get the current board into its goal state. The lower the h-value the better. 

# How to run:
- Have the a_star.py and boards.txt file in the same directory 
- When you hit run it will print the following:
         What boards we read in from the boards.txt file. Of the boards from file which ones are solveable boards. And lastly, the boards we will be solving. Example is below.

![image](https://user-images.githubusercontent.com/50918318/153513529-b6b27831-cd9d-42fd-bb6b-6c31129b5170.png)

- Hit enter to run one board at a time (it will prompt after each board)
- When it's done running it will print the path, path cost, and the number of nodes expanded

![image](https://user-images.githubusercontent.com/50918318/153513553-f93d27fc-615e-4b56-b2ec-03c376b27b00.png)

# Extra Credit
This works by having the user input their own start and goal nodes. Per the assignment instructions we are under the assumption that the board is solveable. 
![image](https://user-images.githubusercontent.com/50918318/153525991-ccecc985-c16f-4af2-8f53-51eafc998197.png)
