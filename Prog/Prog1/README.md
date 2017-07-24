# Programming track - Challange #1

Our challange is to write some code that solves a maze.

The code translates the textual maze into a 2D array, then scans recursively from the starting point in all 4 directions (checking them clock-wise), adding the appropriate character ('>', 'V', '<', '^') to the *steps* string for each successful move.

When the exit is found, the *steps* strings is reversed and this is the solution.

The code also includes an option to solve localy-stored mazes which I used for debugging.
