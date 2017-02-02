# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Constraint propagation in case of naked twins is used as mechanism to eliminate "characters in twins found" in each unit.
   First, we find the twin value, then each character of this twin is eliminated in all the boxes of the unit under consideration.
   While making sure, we do not remove chars in twin from the twins itself.
   This same approach, "find twins and removed twin's chars in non-twin boxes" get repeated for each unit.
   Here as we can see, output of each run, is "capitalized" by next unit as they have less digits in boxes to deal with.
   Which means much small search space to be tried with less possible combinations.
   So, we can see that this constraint of "naked twins" only in unit, gets propagated across units.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: In case of diagonal sudoku, this constraint is same as it is for rows, columns or squares, e.i. unique digit.
   But, because this constraint applied for rows, columns and squared, the search tree of diagonals reduces dramatically.
   Which means diagonals start getting solved as part of constraint applied in other units. So, to solve for diagonals,
   we just add them to units to be considered for uniqueness, and it gets solved as one more constraint spaces added.


### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.