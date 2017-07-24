# Programming track - Challange #2

Our challange is to write some code that splays Connect-4 agains the server.

The challange here is to out-smart the "evolving" server, but also be fast enough, as there is a time limit on our processing time.

The code uses a simple MiniMax implementation with a depth limit of 3 moves, which is not optimal but is required, probably because the implementation is not very optimized.

Main loop
```python
def main():
    conn = socket.create_connection(C4_SERVER)
    response = conn.recv(RECV_SIZE)
    game = connect4()
    random.seed()
    
    while True:
        print response
        if 'Skeelz' not in response:
            return

        # Do a thing here.
        game.read_board(response)
        move = str(minimax(game, 3))
        print move
        if not len(move):
            return
        conn.send(move)
        response = conn.recv(RECV_SIZE)
```

The board is converted from ASCII into a 2D array
```python
class connect4:
    board = None
    
    def __init__(self):
        self.board = None
        
    def read_board(self, response):
        response_lines = response.splitlines()
        find_delim = [x for x in response_lines if x.startswith('Skeelz')][0]
        board_lines = response_lines[response_lines.index(find_delim)+2:-1]
        board_lines = [l.split('|') for l in board_lines if l.startswith('|')]
    
        w = 7
        h = 6
        self.board = [[board_lines[y][x+1].strip() for x in range(w)] for y in range(h)]
```

Simple MiniMax implementation with recursion-depth limit
```python
def minimax(game_state, depth):
    if game_state.is_empty():
        sys.stdout.write('random\n')
        return random.randint(0, 6)

    must = game_state.must_block()
    if must >= 0:
        sys.stdout.write('must %d\n' % must)
        return must

    moves = game_state.get_available_moves()
    best_move = moves[0]#random.randint(0, len(moves)-1)]
    best_score = float('-inf')
    for move in moves:
        clone = game_state.next_state(move, 'x')
        score = min_play(clone, depth-1)
        sys.stdout.write('%d ' % score)
        if score > best_score:
            best_move = move
            best_score = score
    sys.stdout.write('\n')
    return best_move

def min_play(game_state, depth):
    over = False
    player = ''
    if depth > 0:
        (over, player) = game_state.is_gameover()
    if over or depth == 0:
        return evaluate(game_state, player)
    moves = game_state.get_available_moves()
    best_score = float('inf')
    for move in moves:
        clone = game_state.next_state(move, 'o')
        score = max_play(clone, depth-1)
        if score < best_score:
            best_move = move
            best_score = score
    return best_score

def max_play(game_state, depth):
    over = False
    player = ''
    if depth > 0:
        (over, player) = game_state.is_gameover()
    if over or depth == 0:
        return evaluate(game_state, player)
    moves = game_state.get_available_moves()
    best_score = float('-inf')
    for move in moves:
        clone = game_state.next_state(move, 'x')
        score = min_play(clone, depth-1)
        if score > best_score:
            best_move = move
            best_score = score
    return best_score
```

Board evaluation function
```python
def evaluate(game_state, player):
    if player == 'x':
        return 10000
    if player == 'o':
        return -10000

    goodness = game_state.score('x')
    badness = game_state.score('o')

    return goodness - badness
```

Scoring the board uses 2 heuristics
1. the basic score is _4-in-a-row\*10000 + 3-in-a-rows\*1000 + 2-in-a-rows\*100_
2. if the oponent has 3-in-a-row that we can block then we MUST block

This is a little crude, but it got the job done :-)
