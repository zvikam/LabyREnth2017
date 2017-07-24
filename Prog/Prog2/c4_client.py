import socket
import sys
import copy
import random

C4_SERVER = ('52.40.187.77', 16000)
RECV_SIZE = 4096
MAX_STACK = 2000

board = None

class connect4:
    board = None
    
    def __init__(self):
        self.board = None
        
    def display(self):
        w = len(self.board[0])
        h = len(self.board)
        for y in range(h):
            for x in range(w):
                sys.stdout.write('<%s>' % self.board[y][x])
            sys.stdout.write('\n')

    def read_board(self, response):
        response_lines = response.splitlines()
        find_delim = [x for x in response_lines if x.startswith('Skeelz')][0]
        board_lines = response_lines[response_lines.index(find_delim)+2:-1]
        board_lines = [l.split('|') for l in board_lines if l.startswith('|')]
    
        w = 7
        h = 6
        self.board = [[board_lines[y][x+1].strip() for x in range(w)] for y in range(h)]

    @staticmethod
    def score_set(four):
        x = 0
        o = 0
        for i in range(4):
            if four[i] == 'x':
                x += 1
            elif four[i] == 'o':
                o += 1
        if x > 0 and o == 0:
            return x, 'x'
        elif o > 0 and x == 0:
            return o, 'o'
        return 0, ''

    def is_gameover(self):
        w = len(self.board[0])
        h = len(self.board)
        # |
        for y in range(h-3):
            for x in range(w):
                (score, c) = connect4.score_set([self.board[y][x],self.board[y+1][x],self.board[y+2][x],self.board[y+3][x]])
                if score == 4:
                    return True, c
        # -
        for x in range(w-3):
            for y in range(h):
                (score, c) = connect4.score_set([self.board[y][x],self.board[y][x+1],self.board[y][x+2],self.board[y][x+3]])
                if score == 4:
                    return True, c
        # /
        for y in range(h-3):
            for x in range(3, w):
                (score, c) = connect4.score_set([self.board[y][x],self.board[y+1][x-1],self.board[y+2][x-2],self.board[y+3][x-3]])
                if score == 4:
                    return True, c
        # \
        for y in range(3, h):
            for x in range(3, w):
                (score, c) = connect4.score_set([self.board[y][x],self.board[y-1][x-1],self.board[y-2][x-2],self.board[y-3][x-3]])
                if score == 4:
                    return True, c
        return False, ''
    
    @staticmethod
    def find_hole(four):
        for i in range(4):
            if four[i] == '':
                return i
        return -1

    def must_block(self):
        w = len(self.board[0])
        h = len(self.board)
        # |
        for y in range(h-3):
            for x in range(w):
                four = [self.board[y][x],self.board[y+1][x],self.board[y+2][x],self.board[y+3][x]]
                (score, c) = connect4.score_set(four)
                if score == 3:
                    return x
        # -
        for x in range(w-3):
            for y in range(h):
                four = [self.board[y][x],self.board[y][x+1],self.board[y][x+2],self.board[y][x+3]]
                (score, c) = connect4.score_set(four)
                if score == 3:
                    m = x+connect4.find_hole(four)
                    if self.get_row_move(m) == y:
                        return m
        # /
        for y in range(h-3):
            for x in range(3, w):
                four = [self.board[y][x],self.board[y+1][x-1],self.board[y+2][x-2],self.board[y+3][x-3]]
                (score, c) = connect4.score_set(four)
                if score == 3:
                    m = x-connect4.find_hole(four)
                    if self.get_row_move(m) == y+m:
                        return m
        # \
        for y in range(3, h):
            for x in range(3, w):
                four = [self.board[y][x],self.board[y-1][x-1],self.board[y-2][x-2],self.board[y-3][x-3]]
                (score, c) = connect4.score_set(four)
                if score == 3:
                    m = x-connect4.find_hole(four)
                    if self.get_row_move(m) == y-m:
                        return m
        return -1

    def score(self, player):
        total = 0
        w = len(self.board[0])
        h = len(self.board)
        # |
        for y in range(h-3):
            for x in range(w):
                four = [self.board[y][x],self.board[y+1][x],self.board[y+2][x],self.board[y+3][x]]
                (score, c) = connect4.score_set(four)
                if c == player and score > 1:
                    total += 10 ** score 
        # -
        for x in range(w-3):
            for y in range(h):
                four = [self.board[y][x],self.board[y][x+1],self.board[y][x+2],self.board[y][x+3]]
                (score, c) = connect4.score_set(four)
                if c == player and score > 1:
                    total += 10 ** score
        # /
        for y in range(h-3):
            for x in range(3, w):
                four = [self.board[y][x],self.board[y+1][x-1],self.board[y+2][x-2],self.board[y+3][x-3]]
                (score, c) = connect4.score_set(four)
                if c == player and score > 1:
                    total += 10 ** score
        # \
        for y in range(3, h):
            for x in range(3, w):
                four = [self.board[y][x],self.board[y-1][x-1],self.board[y-2][x-2],self.board[y-3][x-3]]
                (score, c) = connect4.score_set(four)
                if c == player and score > 1:
                    total += 10 ** score
        return total
    
    def is_empty(self):
        w = len(self.board[0])
        h = len(self.board)
        for y in range(h):
            for x in range(w):
                if not self.board[y][x] == '':
                    return False
        return True

    def clone(self, other):
        w = len(other.board[0])
        h = len(other.board)
        self.board = [[other.board[y][x] for x in range(w)] for y in range(h)]

    def get_row_move(self, move):
        h = len(self.board)
        for y in range(h-1,0,-1):
            if self.board[y][move] == '':
                return y
        return -1
    
    def move(self, move, player):
        self.board[self.get_row_move(move)][move] = player
        
    def next_state(self, move, player):
        new_state = connect4()
        new_state.clone(self)
        new_state.move(move, player)
        return new_state

    def get_available_moves(self):
        moves = []
        w = len(self.board[0])
        for x in range(w):
            if self.board[0][x] == '':
                moves.append(x)
        return moves

def evaluate(game_state, player):
    if player == 'x':
        return 10000
    if player == 'o':
        return -10000
    
    goodness = game_state.score('x')
    badness = game_state.score('o')
    
    return goodness - badness

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
        sys.setrecursionlimit(MAX_STACK*2)
        move = str(minimax(game, 3))
        print move
        if not len(move):
            return
        conn.send(move)
        response = conn.recv(RECV_SIZE)


if __name__ == '__main__':
    main()
