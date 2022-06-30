import sys
from operator import pos
import numpy as np
import random
import time
from numpy import indices
from copy import deepcopy
import pygame
import math

from connect4 import COLUMN_COUNT

class connect4Player(object):
	def __init__(self, position, seed=0):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)

	def play(self, env, move):
		move = [-1]

class human(connect4Player):

	def play(self, env, move):
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env, move):
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
					else:
						pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)

class stupidAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]

class minimaxAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		MAXI = [-math.inf,-math.inf,-math.inf,-math.inf,-math.inf,-math.inf,-math.inf]
		if len(env.history[0]) == 0:
			move[:] = [3]
			return
		player = self.position
		for i,p in enumerate(possible):
			if p == False :
				continue
			depth = 2
			newboard = deepcopy(env)
			MAXI[i] = self.MIN_VALUE(newboard, depth, i, player)

		move[:] = [MAXI.index(max(MAXI))]



	def MIN_VALUE(self, env, depth, move, player):
		switch = {1:2,2:1}
		self.simulateMove(env, move, player)
		if env.gameOver(move, player):
			return math.inf
		if depth == 0:
			return self.evaluation(env.getBoard())
		player = switch[player]
		possible = env.topPosition >= 0
		v = math.inf
		moves = [i for i, p in enumerate(possible) if p]
		for i,p in enumerate(possible):
			if p == False : continue
			newboard = deepcopy(env)
			v = min(v, self.MAX_VALUE(newboard, depth - 1, i, player))
		return v

	def MAX_VALUE(self, env, depth, move, player):
		switch = {1:2,2:1}
		self.simulateMove(env, move, player)
		if env.gameOver(move, player): return -(math.inf)
		if depth == 0:
			return self.evaluation(env.getBoard())
		player = switch[player]
		possible = env.topPosition >= 0
		v = -math.inf
		moves = [i for i, p in enumerate(possible) if p]
		for i,p in enumerate(possible):
			if p == False : continue
			newboard = deepcopy(env)
			v = max(v, self.MIN_VALUE(newboard, depth - 1, i, player))
		return v


	def evaluation(self, board):
	    eval =0
	    col = [row[3] for row in board]
	    eval += col.count(self.position)*5
	    col = [row[4] for row in board]
	    eval += col.count(self.position)*3
	    col = [row[2] for row in board]
	    eval += col.count(self.position)*3

	    return eval

	def simulateMove(self, env, move, player):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)



class alphaBetaAI(connect4Player):

	def play(self, env, move):


		possible = env.topPosition >= 0
		MAXI = [-math.inf,-math.inf,-math.inf,-math.inf,-math.inf,-math.inf,-math.inf]
		if len(env.history[0]) == 0:
			move[:] = [3]
			return
		player = self.position
		for i,p in enumerate(possible):
			if p == False :
				continue
			depth = 2
			newboard = deepcopy(env)
			MAXI[i] = self.MIN_VALUE(newboard, depth, i, player, -math.inf, math.inf)

		move[:] = [MAXI.index(max(MAXI))]


	def MIN_VALUE(self, env, depth, move, player, alpha, beta):

		switch = {1:2,2:1}
		minSuccessor = {0, 6, 1, 5, 2, 4, 3}
		self.simulateMove(env, move, player)
		if env.gameOver(move, player):
			return math.inf
		if depth == 0:
			return self.evaluation(env.getBoard())
		player = switch[player]
		possible = env.topPosition >= 0
		v = math.inf

		for i, p in enumerate(possible):
			for j in minSuccessor:
				if not (p == i): continue
				newboard = deepcopy(env)
				v = min(v, self.MAX_VALUE(newboard, depth - 1, j, player, alpha, beta))
				if (alpha >= v):
					return v
				beta = min(beta, v)
		return v

	def MAX_VALUE(self, env, depth, move, player, alpha, beta):

		switch = {1:2,2:1}
		maxSuccessor = {3, 2, 4, 1, 5, 0, 6}
		self.simulateMove(env, move, player)
		if env.gameOver(move, player): return -(math.inf)
		if depth == 0:
			return self.evaluation(env.getBoard())
		player = switch[player]
		possible = env.topPosition >= 0
		v = -math.inf


		for j, p in enumerate(possible):
			for i in maxSuccessor:
				if not (p == i): continue
				newboard = deepcopy(env)
				v = max(v, self.MIN_VALUE(newboard, depth - 1, i, player, alpha, beta))
				if (beta <= v):
					return v
				alpha = max(alpha, v)
		return v

	def evaluation(self, board):
	    eval =0
	    center = [row[3] for row in board]
	    eval += center.count(self.position)*5
	    center = [row[4] for row in board]
	    eval += center.count(self.position)*3
	    center = [row[2] for row in board]
	    eval += center.count(self.position)*3

	    return eval

	def simulateMove(self, env, move, player):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)



SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)






