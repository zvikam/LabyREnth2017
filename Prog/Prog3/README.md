# Programming track - Challange #3 [PARTIAL]

Our challange is to write some code that solves a maze, but there are a couple of "extra" caveats:

1. the interface represent a 1st-person view of the maze
2. the maze cheats...

## NOTE
This article and code do not provide a complete solution to the challange.

I never actually figured out the logic behind the maze's cheating. But I think the code provided is stil interesting.


## Navigating the maze

Unlike the 1st challange, we don't get a complete map of the maze.

Even more challanging, we get to see the maze from a 1st-person view point, so our challanges are 

1. build the map of the maze given what we see in front of us at any point
2. try and navigate the section of the map we have in a way similar to challange #1
3. translate our movements from 3rd-person to 1st person and vice versa
4. most important - the maze cheats - walls will appear at (non-)random places, where there once was a passage.

1st of all, let's complete the code that communicates with the server.
I had to modify the original code to handle cases where a response would be split between to socket 'recv' operations
```python
import socket
import sys

MAZE_SERVER = ('34.211.117.64', 16000)
RECV_SIZE = 8192

def main():
    conn = socket.create_connection(MAZE_SERVER)
    response = conn.recv(RECV_SIZE)

    complete = False
    cont = False

    while True:
        print response
        complete = False
        # Do a thing here.
        response_lines = response.splitlines()
        if cont and not complete:
            complete = True
            cont = False

        if response_lines[0].startswith('Invalid movement'):
            return

        if response_lines[0].startswith('-----------------------------------------'):
            wall = True

        if response_lines[len(response_lines)-1].startswith('-----------------------------------------') or response_lines[len(response_lines)-1].startswith('The possible moves are'):
            complete = True

        if not complete:
            cont = True
            print "damn socket"
        else:
            conn.send(move)

        response = conn.recv(RECV_SIZE)

if __name__ == '__main__':
    main()
```
Let's define a few auxiliary variables that will help us while we navigate the maze
```python
# location changes when moving in each direction [ X-diff, Y-diff ]
directions = [ [0,-1], [1,0], [0,1], [-1,0] ]
# direction names in human-readable format
dirnames = [ '^', '>', 'V', '<' ]
# initial direction is RIGHT ('>')
direction = 1
# initial location
location = [ 1, 1 ]
```
We define our maze anarbitrary initial size of 64x64, where the upper left corner is (0,0) and X grows to the right (and Y grows 'down), so we start at (1,1).
Each cell is a char representing its content:
* '#' = wall
* '.' = corridor, unvisited
* 'o' = corridor, visited
* 'X' = dead-end
* '^', '>', 'V', '<' = player
```python
w = 64
h = 64
maze = [['.' for x in range(w)] for y in range(h)]
maze[location[1]][location[0]] = dirnames[direction]
```
We also keep a "shadow" copy of the maze with a counter of how many times we visited each cell. This helps us decide which direction to go when faced with multiple corridors.
```python
visits = [[0 for x in range(w)] for y in range(h)]
visits[location[1]][location[0]] = 1
```
Next, we'll check the response the server gave us and update our 2D map accordingly.
```python
for x in response_lines:
    if x.startswith('Ahead you see'):
        wall = False
        if x.startswith('Ahead you see a hallway'):
            d = direction
            newloc = [location[0]+directions[d][0],location[1]+directions[d][1]]
            d = (direction + 1) % len(directions)
            maze[newloc[1]+directions[d][1]][newloc[0]+directions[d][0]] = '#'
            d = (direction + len(directions) - 1) % len(directions)
            maze[newloc[1]+directions[d][1]][newloc[0]+directions[d][0]] = '#'
            pass
        elif x.startswith('Ahead you see some turns'):
            pass
        elif x.startswith('Ahead you see a right turn'):
            d = direction
            newloc = [location[0]+directions[d][0],location[1]+directions[d][1]]
            d = (direction + len(directions) - 1) % len(directions)
            maze[newloc[1]+directions[d][1]][newloc[0]+directions[d][0]] = '#'
            pass
        elif x.startswith('Ahead you see a left turn'):
            d = direction
            newloc = [location[0]+directions[d][0],location[1]+directions[d][1]]
            d = (direction + 1) % len(directions)
            maze[newloc[1]+directions[d][1]][newloc[0]+directions[d][0]] = '#'
            pass
        elif x.startswith('Ahead you see a dead end'):
            d = direction
            maze[location[1]+directions[d][1]][location[0]+directions[d][0]] = 'X'
            newloc = [location[0]+directions[d][0],location[1]+directions[d][1]]
            maze[newloc[1]+directions[d][1]][newloc[0]+directions[d][0]] = '#'
            d = (direction + 1) % len(directions)
            maze[newloc[1]+directions[d][1]][newloc[0]+directions[d][0]] = '#'
            d = (direction + len(directions) - 1) % len(directions)
            maze[newloc[1]+directions[d][1]][newloc[0]+directions[d][0]] = '#'
            pass
    elif x.startswith('Invalid movement'):
        return
```
Note that in order to turn right, we need to `+1` our `direction` variable, while in order to turn left we `-1`. Since we need to keep the direction inside the range `[0,3]`, we notice 2 things:
1. we must use the modulo operator `%` to wrap around the boundary
2. as a result, `-1` is identical to `+3`

So turning *right* becomes `new_direction = (direction + 1) % len(directions)` while turning *left* is `new_direction = (direction + len(directions) - 1) % len(directions)`.

After we've updated the maze, we need to figure out where we should go next. We check all the cells around our current location, and grade them according to the information we have. We then choose the cell with the lowest score.
```python
grade = []
for i in [0, 1, 3, 2]:
    # find out where we've never been and go there
    d = (direction + i) % len(directions)
    c = maze[location[1]+directions[d][1]][location[0]+directions[d][0]];
    v = visits[location[1]+directions[d][1]][location[0]+directions[d][0]];
    g = { '#': 9999, 'o': v, '.': 0, 'X': 9998}[c]
    grade.append({'dir': i, 'grade': g})
m = min(grade, key=lambda k: k['grade'])
if m['grade'] == 9999:
    print "STUCK!"
    return
moves.append(valid_moves[m['dir']])
```
In case we're sorrounded by walls (because the game cheats!!!), we just give up.

**NOTE**: This is where we should have added some logic to detect the impending "cheat" and avoid it.

The last step is to act according to the selected step
```python
# mark current location as visited
maze[location[1]][location[0]] = 'o'
# increment visits counter
visits[location[1]][location[0]] += 1
if move == 'w':
    # walk forward, but don't walk into a wall
    if not wall:
        location[0] += directions[direction][0]
        location[1] += directions[direction][1]
if move == 's':
    # walk backwards
    visits[location[1]][location[0]] += 1
    location[0] -= directions[direction][0]
    location[1] -= directions[direction][1]
elif move == 'd':
    # turn right
    direction = (direction + 1) % len(directions)
elif move == 'a':
    # turn left
    direction = (direction + len(directions) - 1) % len(directions)

# update player's 'icon' to match facing direction
maze[location[1]][location[0]] = dirnames[direction]

allmoves.append(move)
conn.send(move)
move_count += 1
```
... and that's as far as I got.
