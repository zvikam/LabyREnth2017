# Programming track - Challange #3 [PARTIAL]

Our challange is to write some code that solves a maze, but there are a couple of "extra" caveats:

1. the interface represent a 1st-person view of the maze
2. the maze cheats...

## NOTE
This article and code do not provide a complete solution to the challange.

I never actually figured out the logic behind the maze's cheating. But I think the code provided is stil interesting.

At first I thought my algorithm wasn't smart enough so the server is "punishing" me, so I tried to add tests and heuristics to predict wall locations and avoid dead-ends, but that turned out to be ... a dead-end :-)

I also thought the cheats were time related (either "time between moves" or "time since start of execution"), but I could not find the logic there as well.


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

