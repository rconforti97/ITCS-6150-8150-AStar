Rachel Conforti
ITCS 6150 - Intelligent Systems Readme

Algorithm: A*

- How to run my program:
Open a ide that runs python (Spyder, VS, etc.)
Run the file a_star.py
Press ENTER between each board to have the program run the passed in boards

Ensure you have the following imports - numpy, copy, and queue. These are 
very common imports so this should not be an issue. 

- What to expect:
I coded my A* algorithm to automatically read in the boards and to wait for the user
to hit 'Enter' before preceeding to the next board to allow the TA's/Professor time 
to look at the path, the expanded nodes number, and the path cost.

- Extra Credit:
The extra credit portion will automatically start after the last board is finished.*(look at Known Issues section)
It will ask for you to input the start board and goal node and will automatically run the A* algorithm.
If you do not wish to wait for the last board to solve, please comment out lines 238 through 249 and re-run 
the program. 
Enter the boards into the console like so: x,x,x,x,x,x,x,x,x


- *Known Issues:
My code will solve the last solveable board [8, 3, 0, 5, 6, 1, 7, 4, 2]. However, it is
currently solving around the 16 minute mark. I understand that is to long, but the program
will solve it, if you have the time to wait.

Github link to project: https://github.com/rconforti97/ITCS-6150-8150-AStar