import socket
import pprint
import datetime
import random
import time
import sys

MAZE_SERVER = ('34.211.117.64', 16000)
RECV_SIZE = 8192

valid_moves = ['w', 'd', 'a', 'a' ]
cheats = []

def display(maze):
	w = len(maze[0])
	h = len(maze)
	for y in range(h):
		for x in range(w):
			sys.stdout.write('%s' % maze[y][x])
		sys.stdout.write('\n')
	sys.stdout.write('\n')

def main():
	global cheats
	random.seed()
	conn = socket.create_connection(MAZE_SERVER)
	response = conn.recv(RECV_SIZE)

	allmoves = []
	moves = []
	complete = False
	directions = [ [0,-1], [1,0], [0,1], [-1,0] ]
	dirnames = [ '^', '>', 'V', '<' ]
	direction = 1
	location = [ 1, 1 ]
	wall = False
	cont = False
	same_loc = 0
	move_count = 0
	
	w = 64
	h = 32
	maze = [['.' for x in range(w)] for y in range(h)]
	maze[location[1]][location[0]] = dirnames[direction]
	visits = [[0 for x in range(w)] for y in range(h)]
	visits[location[1]][location[0]] = 1
	
	start = datetime.datetime.now()
	while True:
		#now = datetime.datetime.now()
		print response
		#print time.asctime()
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
			# if there wasn't a wall there before... it's cheating
			if maze[location[1]+directions[direction][1]][location[0]+directions[direction][0]] == 'o':
				cheats.append({'time': now, 'relative_time': now-start, 'moves': move_count, 'location': [location[1]+directions[direction][1], location[0]+directions[direction][0]] })
				pass
			maze[location[1]+directions[direction][1]][location[0]+directions[direction][0]] = '#'

		if response_lines[len(response_lines)-1].startswith('-----------------------------------------') or response_lines[len(response_lines)-1].startswith('The possible moves are') or len(response_lines) == 22:
			complete = True

		if not complete:
			cont = True
			print "damn socket"
		else:
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
			
			display(maze)
			if len(moves) == 0:
				grade = []
				for i in [0, 1, 3, 2]:
					# find out where we've never been and go there
					d = (direction + i) % len(directions)
					c = maze[location[1]+directions[d][1]][location[0]+directions[d][0]];
					v = visits[location[1]+directions[d][1]][location[0]+directions[d][0]];
					g = { '#': 9999, 'o': v, '.': 0, 'X': 9998}[c]
					grade.append({'dir': i, 'grade': g})
				m = min(grade, key=lambda k: k['grade'])
				print grade, m
				#time.sleep(1)
				if m['grade'] == 9999:
					print "STUCK!"
					return
				moves.append(valid_moves[m['dir']])
				
			#print moves
			if len(moves) > 0:
				move = moves.pop()
			else:
				#move = valid_moves[random.randint(0, 3)]
				#move = raw_input("Your Move: ")
				pass
			if not len(move):
				return
			
			maze[location[1]][location[0]] = 'o'
			visits[location[1]][location[0]] += 1
			if move == 'w':
				if not wall:
					same_loc = 0
					location[0] += directions[direction][0]
					location[1] += directions[direction][1]
				else:
					same_loc += 1
			if move == 's':
				same_loc = 0
				visits[location[1]][location[0]] += 1
				location[0] -= directions[direction][0]
				location[1] -= directions[direction][1]
			elif move == 'd':
				same_loc += 1
				direction = (direction + 1) % len(directions)
			elif move == 'a':
				same_loc += 1
				direction = (direction + len(directions) - 1) % len(directions)
			
			maze[location[1]][location[0]] = dirnames[direction]
			
			if same_loc > 8:
				print "STUCK!"
				move = 'q'
			
			allmoves.append(move)
			#print allmoves
			conn.send(move)
			move_count += 1
		response = conn.recv(RECV_SIZE)

if __name__ == '__main__':
	main()
	#pp = pprint.PrettyPrinter(indent=4)
	#pp.pprint(cheats)
	
