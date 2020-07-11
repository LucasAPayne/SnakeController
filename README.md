# SnakeController

SnakeController uses the Pygame module for Python and methods of graph theory (namely Hamiltonian cycles) to win at Snake. It represents the game world as a graph and generates
an optimal path around it so that the snake never runs into its tail. Currently, the solution is limited to only square grids and the backtracking method for finding Hamiltonian 
cycles. However, as development continues, there will be several more options for solving this problem.

## Future Features
- Support for manual input
- Different methods for finding Hamiltonian cycles
- Performance logging to compare the efficiency of the different methods
- Additional visual effects (post-processing)
- A settings menu, complete with GUI, to manipulate several parts of the solution, including many of those listed above

### Known Issues
- The game sometimes becomes unresponsive just as it is won.
  - Appears to be caused by moving the window while the main game loop is running
