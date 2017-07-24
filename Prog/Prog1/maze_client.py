import sys
import time
from socket import create_connection

MAZE_SERVER = ('54.69.145.229', 16000)
RECV_SIZE = 8192

steps = ''
maze = None
def log(s):
    #sys.stdout.write(s)
    pass

def search(x, y, step):
    global steps 
    global maze
    
    #display(maze)
    #time.sleep(0.1)

    if maze[y][x] == 'X':
        log('found at %d,%d\n' % (x, y))
        steps += step
        return True
    elif maze[y][x] == '#':
        log('wall at %d,%d\n' % (x, y))
        return False
    elif maze[y][x] == 'o':
        log('visited at %d,%d\n' % (x, y))
        return False
     
    log('visiting %d,%d\n' % (x, y))
 
    # mark as visited
    maze[y][x] = 'o'
 
    # explore neighbors clockwise starting by the one on the right
    if ((x < len(maze[0])-1 and search(x+1, y, '>'))
        or (x > 0 and search(x-1, y, '<'))
        or (y > 0 and search(x, y-1, '^'))
        or (y < len(maze)-1 and search(x, y+1, 'V'))):
        steps += step
        return True
 
    return False
 
def display(maze):
    w = len(maze[0])
    h = len(maze)
    for y in range(h):
        for x in range(w):
            sys.stdout.write('%s' % maze[y][x])
        sys.stdout.write('\n')

def solve(maze_lines):
    #print maze_lines
    global maze
    global steps

    steps = ''   
    start = [0,0]
    w = len(maze_lines[0])
    h = len(maze_lines)
    maze = [[0 for x in range(w)] for y in range(h)]
    for y in range(h):
        for x in range(w):
            c = maze_lines[y][x]
            if c == '>':
                start = [y,x]
                c = 'S'
            maze[y][x] = c
    #display(maze)
    search(start[0], start[1], '')
    return steps[::-1]

def main_alt(filename):
    with open(filename) as f:
        maze_lines = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    maze_lines = [x.strip() for x in maze_lines]
    print solve(maze_lines)
    
def main():
    conn = create_connection(MAZE_SERVER)
    response = conn.recv(RECV_SIZE)
    while True:
        print response
        if "Now " not in response:
            return

        response_lines = response.splitlines()
        find_delim = [x for x in response_lines if x.startswith('Now')][0]
        maze_lines = response_lines[response_lines.index(find_delim)+2:-1]
        maze_text = '\n'.join(maze_lines)

        # Do your thing here with either maze_text or maze_lines.

        #solution = raw_input("Your solution: ")
        solution = solve(maze_lines)
        if not len(solution):
            return
        print solution
        conn.send(solution)

        response = conn.recv(RECV_SIZE)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        main_alt(sys.argv[1])
