# Gomoku Project [GomokuBoard]
# B351 - Sreekar Antharam, Daniel Byun, Andrew Chong

import math
import GomokuNeuralNet
import numpy as np
import pickle

class GomokuPlayer:

	def __init__(self, depthLimit, isPlayerOne):
		self.isPlayerOne = isPlayerOne
		self.depthLimit = depthLimit

	def replace(self,array, a, b):
		for i in range(len(array)):
			if array[i] == a:
				array[i] = b
		return array
	
	def heuristicNN(self, board):
		flatArray = self.replace(np.asarray(board.board).flatten(),None,0)
		pickle_in3 = open("gomoku_regressor_fivepattern_andrew.pickle","rb")
		load_regressor = pickle.load(pickle_in3)

		return load_regressor.predict([flatArray])[0]

	def heuristicNN_old(self, board):
		flatArray = self.replace(np.asarray(board.board).flatten(),None,0)
		pickle_in3 = open("gomoku_regressor_update_andrew.pickle","rb")
		load_regressor = pickle.load(pickle_in3)

		return load_regressor.predict([flatArray])[0] 
	
	def dummyHeur(self, board): # dummy heuristic used for testing
		p1Count = 0
		p2Count = 0
		rowList = ["","","","","","","","","","","","","","","","","","",""]
		colList = ["","","","","","","","","","","","","","","","","","",""]
		diagRightList = []
		diagLeftList = []
		
		# ===BUILDING ROWS AND COLUMNS===
		for a in range(board.WIDTH):		# outer loop will keep track of the column
			for b in range(board.HEIGHT):   # innger loop with keep track of the row
				if len(board.board[a]) > b: # if the length of the current column is larger than our current row iterator, continue
					if board.board[a][b] == 0:	  # Player 1
						colList[a] += "0"
						rowList[b] += "0"
					elif board.board[a][b] == 1:	# Player 2
						colList[a] += "@"
						rowList[b] += "@"
					else:
						colList[a] += "_"
						rowList[b] += "_"
				else:					   # else we should add "_" since there is nothing there
					colList[a] += "_"
					rowList[b] += "_"
		
		for a in range(19):  # the diagonal will never exceed 19 values
			currentList = ""
			currentList2= ""
			currentList3= ""
			currentList4= ""
			currentPos = (0,a)  # first: iterate through left column for right
			currentPos2= (a,0)
			currentPos3= (19,a)
			currentPos4= (a,0)
			while(board.inRange(currentPos) or board.inRange(currentPos2) or board.inRange(currentPos3) or board.inRange(currentPos4)):
				if board.inRange(currentPos):
					try:
						if board.board[currentPos[0]][currentPos[1]] == 0:
							currentList += "0"
						elif board.board[currentPos[0]][currentPos[1]] == 1:
							currentList += "@"
						else:
							currentList += "_"
						currentPos = (currentPos[0]+1,currentPos[1]+1)
					except:
						currentList += "_"
						currentPos = (currentPos[0]+1,currentPos[1]+1)
				if board.inRange(currentPos2):
					try:
						if board.board[currentPos2[0]][currentPos2[1]] == 0:
							currentList2 += "0"
						elif board.board[currentPos2[0]][currentPos2[1]] == 1:
							currentList2 += "@"
						else:
							currentList2 += "_"
						currentPos2 = (currentPos2[0]+1,currentPos2[1]+1)
					except:
						currentList2 += "_"
						currentPos2 = (currentPos2[0]+1,currentPos2[1]+1)
				if board.inRange(currentPos3):
					try:
						if board.board[currentPos3[0]][currentPos3[1]] == 0:
							currentList3 += "0"
						elif board.board[currentPos3[0]][currentPos3[1]] == 1:
							currentList3 += "@"
						else:
							currentList3 += "_"
						currentPos3 = (currentPos3[0]-1,currentPos3[1]+1)
					except:
						currentList3 += "_"
						currentPos3 = (currentPos3[0]-1,currentPos3[1]+1)
				if board.inRange(currentPos4):
					try:
						if board.board[currentPos4[0]][currentPos4[1]] == 0:
							currentList4 += "0"
						elif board.board[currentPos4[0]][currentPos4[1]] == 1:
							currentList4 += "@"
						else:
							currentList4 += "_"
						currentPos4 = (currentPos4[0]-1,currentPos4[1]+1)
					except:
						currentList4 += "_"
						currentPos4 = (currentPos4[0]-1,currentPos4[1]+1)
			diagRightList.append(currentList)
			diagRightList.append(currentList2)
			diagRightList.append(currentList3)
			diagRightList.append(currentList4)
		
		# ===CHECKING EACH LIST===
		for a in range(len(diagRightList)):
			try:
				theList=rowList
				while "0" in theList[a] or "@" in theList[a]: # run while there is an 0 or an @ in the current string
					if "0000" in theList[a]:
						theList[a] = theList[a].replace("0000","")
						p1Count += 4
					elif "000" in theList[a]:
						theList[a] = theList[a].replace("000","")
						p1Count += 3
					elif "00" in theList[a]:
						theList[a] = theList[a].replace("00","")
						p1Count += 2
					elif "0" in theList[a]:
						theList[a] = theList[a].replace("0","")
						p1Count += 1
					if "@@@@" in theList[a]:
						theList[a] = theList[a].replace("@@@@","")
						p2Count += 4
					elif "@@@" in theList[a]:
						theList[a] = theList[a].replace("@@@","")
						p2Count += 3
					elif "@@" in theList[a]:
						theList[a] = theList[a].replace("@@","")
						p2Count += 2
					elif "@" in theList[a]:
						theList[a] = theList[a].replace("@","")
						p2Count += 1
			except:
				pass
			try:
				theList=colList
				while "0" in theList[a] or "@" in theList[a]: # run while there is an 0 or an @ in the current string
					if "0000" in theList[a]:
						theList[a] = theList[a].replace("0000","")
						p1Count += 4
					elif "000" in theList[a]:
						theList[a] = theList[a].replace("000","")
						p1Count += 3
					elif "00" in theList[a]:
						theList[a] = theList[a].replace("00","")
						p1Count += 2
					elif "0" in theList[a]:
						theList[a] = theList[a].replace("0","")
						p1Count += 1
					if "@@@@" in theList[a]:
						theList[a] = theList[a].replace("@@@@","")
						p2Count += 4
					elif "@@@" in theList[a]:
						theList[a] = theList[a].replace("@@@","")
						p2Count += 3
					elif "@@" in theList[a]:
						theList[a] = theList[a].replace("@@","")
						p2Count += 2
					elif "@" in theList[a]:
						theList[a] = theList[a].replace("@","")
						p2Count += 1
			except:
				pass
			try:
				theList=diagRightList
				while "0" in theList[a] or "@" in theList[a]: # run while there is an 0 or an @ in the current string
					if "0000" in theList[a]:
						theList[a] = theList[a].replace("0000","")
						p1Count += 4
					elif "000" in theList[a]:
						theList[a] = theList[a].replace("000","")
						p1Count += 3
					elif "00" in theList[a]:
						theList[a] = theList[a].replace("00","")
						p1Count += 2
					elif "0" in theList[a]:
						theList[a] = theList[a].replace("0","")
						p1Count += 1
					if "@@@@" in theList[a]:
						theList[a] = theList[a].replace("@@@@","")
						p2Count += 4
					elif "@@@" in theList[a]:
						theList[a] = theList[a].replace("@@@","")
						p2Count += 3
					elif "@@" in theList[a]:
						theList[a] = theList[a].replace("@@","")
						p2Count += 2
					elif "@" in theList[a]:
						theList[a] = theList[a].replace("@","")
						p2Count += 1
			except:
				pass
			try:
				theList=diagLeftList
				while "0" in theList[a] or "@" in theList[a]: # run while there is an 0 or an @ in the current string
					if "0000" in theList[a]:
						theList[a] = theList[a].replace("0000","")
						p1Count += 4
					elif "000" in theList[a]:
						theList[a] = theList[a].replace("000","")
						p1Count += 3
					elif "00" in theList[a]:
						theList[a] = theList[a].replace("00","")
						p1Count += 2
					elif "0" in theList[a]:
						theList[a] = theList[a].replace("0","")
						p1Count += 1
					if "@@@@" in theList[a]:
						theList[a] = theList[a].replace("@@@@","")
						p2Count += 4
					elif "@@@" in theList[a]:
						theList[a] = theList[a].replace("@@@","")
						p2Count += 3
					elif "@@" in theList[a]:
						theList[a] = theList[a].replace("@@","")
						p2Count += 2
					elif "@" in theList[a]:
						theList[a] = theList[a].replace("@","")
						p2Count += 1
			except:
				pass
		return p1Count - p2Count
	
	def heuristic(self, board): # Heuristic will count up total tiles in a row and assign value
		p1Count = 0
		p2Count = 0
		rowList = ["","","","","","","","","","","","","","","","","","",""]
		colList = ["","","","","","","","","","","","","","","","","","",""]
		diagRightList = []
		diagLeftList = []
		
		# ===BUILDING ROWS AND COLUMNS===
		for a in range(board.WIDTH):		# outer loop will keep track of the column
			for b in range(board.HEIGHT):   # innger loop with keep track of the row
				if len(board.board[a]) > b: # if the length of the current column is larger than our current row iterator, continue
					if board.board[a][b] == 0:	  # Player 1
						colList[a] += "0"
						rowList[b] += "0"
					elif board.board[a][b] == 1:	# Player 2
						colList[a] += "@"
						rowList[b] += "@"
					else:
						colList[a] += "_"
						rowList[b] += "_"
				else:					# else we should add "_" since there is nothing there
					colList[a] += "_"
					rowList[b] += "_"
		
		for a in range(19):  # the diagonal will never exceed 19 values
			currentList = ""
			currentList2= ""
			currentList3= ""
			currentList4= ""
			currentPos = (0,a)  # first: iterate through left column for right
			currentPos2= (a,0)
			currentPos3= (19,a)
			currentPos4= (a,0)
			while(board.inRange(currentPos) or board.inRange(currentPos2) or board.inRange(currentPos3) or board.inRange(currentPos4)):
				if board.inRange(currentPos):
					try:
						if board.board[currentPos[0]][currentPos[1]] == 0:
							currentList += "0"
						elif board.board[currentPos[0]][currentPos[1]] == 1:
							currentList += "@"
						else:
							currentList += "_"
						currentPos = (currentPos[0]+1,currentPos[1]+1)
					except:
						currentList += "_"
						currentPos = (currentPos[0]+1,currentPos[1]+1)
				if board.inRange(currentPos2):
					try:
						if board.board[currentPos2[0]][currentPos2[1]] == 0:
							currentList2 += "0"
						elif board.board[currentPos2[0]][currentPos2[1]] == 1:
							currentList2 += "@"
						else:
							currentList2 += "_"
						currentPos2 = (currentPos2[0]+1,currentPos2[1]+1)
					except:
						currentList2 += "_"
						currentPos2 = (currentPos2[0]+1,currentPos2[1]+1)
				if board.inRange(currentPos3):
					try:
						if board.board[currentPos3[0]][currentPos3[1]] == 0:
							currentList3 += "0"
						elif board.board[currentPos3[0]][currentPos3[1]] == 1:
							currentList3 += "@"
						else:
							currentList3 += "_"
						currentPos3 = (currentPos3[0]-1,currentPos3[1]+1)
					except:
						currentList3 += "_"
						currentPos3 = (currentPos3[0]-1,currentPos3[1]+1)
				if board.inRange(currentPos4):
					try:
						if board.board[currentPos4[0]][currentPos4[1]] == 0:
							currentList4 += "0"
						elif board.board[currentPos4[0]][currentPos4[1]] == 1:
							currentList4 += "@"
						else:
							currentList4 += "_"
						currentPos4 = (currentPos4[0]-1,currentPos4[1]+1)
					except:
						currentList4 += "_"
						currentPos4 = (currentPos4[0]-1,currentPos4[1]+1)
			diagRightList.append(currentList)
			diagRightList.append(currentList2)
			diagRightList.append(currentList3)
			diagRightList.append(currentList4)
		
		# ===CHECKING EACH LIST===
		for a in range(len(diagRightList)):
			try:
				theList=rowList
				while "0" in theList[a] or "@" in theList[a]: # run while there is an 0 or an @ in the current string
					if "0000" in theList[a]:
						theList[a] = theList[a].replace("0000","")
						p1Count += 500
					elif "000" in theList[a]:
						theList[a] = theList[a].replace("000","")
						p1Count += 200
					elif "00" in theList[a]:
						theList[a] = theList[a].replace("00","")
						p1Count += 50
					elif "0" in theList[a]:
						theList[a] = theList[a].replace("0","")
						p1Count += 1
					if "@@@@" in theList[a]:
						theList[a] = theList[a].replace("@@@@","")
						p2Count += 500
					elif "@@@" in theList[a]:
						theList[a] = theList[a].replace("@@@","")
						p2Count += 200
					elif "@@" in theList[a]:
						theList[a] = theList[a].replace("@@","")
						p2Count += 50
					elif "@" in theList[a]:
						theList[a] = theList[a].replace("@","")
						p2Count += 1
			except:
				pass
			try:
				theList=colList
				while "0" in theList[a] or "@" in theList[a]: # run while there is an 0 or an @ in the current string
					if "0000" in theList[a]:
						theList[a] = theList[a].replace("0000","")
						p1Count += 500
					elif "000" in theList[a]:
						theList[a] = theList[a].replace("000","")
						p1Count += 200
					elif "00" in theList[a]:
						theList[a] = theList[a].replace("00","")
						p1Count += 50
					elif "0" in theList[a]:
						theList[a] = theList[a].replace("0","")
						p1Count += 1
					if "@@@@" in theList[a]:
						theList[a] = theList[a].replace("@@@@","")
						p2Count += 500
					elif "@@@" in theList[a]:
						theList[a] = theList[a].replace("@@@","")
						p2Count += 200
					elif "@@" in theList[a]:
						theList[a] = theList[a].replace("@@","")
						p2Count += 50
					elif "@" in theList[a]:
						theList[a] = theList[a].replace("@","")
						p2Count += 1
			except:
				pass
			try:
				theList=diagRightList
				while "0" in theList[a] or "@" in theList[a]: # run while there is an 0 or an @ in the current string
					if "0000" in theList[a]:
						theList[a] = theList[a].replace("0000","")
						p1Count += 500
					elif "000" in theList[a]:
						theList[a] = theList[a].replace("000","")
						p1Count += 200
					elif "00" in theList[a]:
						theList[a] = theList[a].replace("00","")
						p1Count += 50
					elif "0" in theList[a]:
						theList[a] = theList[a].replace("0","")
						p1Count += 1
					if "@@@@" in theList[a]:
						theList[a] = theList[a].replace("@@@@","")
						p2Count += 500
					elif "@@@" in theList[a]:
						theList[a] = theList[a].replace("@@@","")
						p2Count += 200
					elif "@@" in theList[a]:
						theList[a] = theList[a].replace("@@","")
						p2Count += 50
					elif "@" in theList[a]:
						theList[a] = theList[a].replace("@","")
						p2Count += 1
			except:
				pass
			try:
				theList=diagLeftList
				while "0" in theList[a] or "@" in theList[a]: # run while there is an 0 or an @ in the current string
					if "0000" in theList[a]:
						theList[a] = theList[a].replace("0000","")
						p1Count += 500
					elif "000" in theList[a]:
						theList[a] = theList[a].replace("000","")
						p1Count += 200
					elif "00" in theList[a]:
						theList[a] = theList[a].replace("00","")
						p1Count += 50
					elif "0" in theList[a]:
						theList[a] = theList[a].replace("0","")
						p1Count += 1
					if "@@@@" in theList[a]:
						theList[a] = theList[a].replace("@@@@","")
						p2Count += 500
					elif "@@@" in theList[a]:
						theList[a] = theList[a].replace("@@@","")
						p2Count += 200
					elif "@@" in theList[a]:
						theList[a] = theList[a].replace("@@","")
						p2Count += 50
					elif "@" in theList[a]:
						theList[a] = theList[a].replace("@","")
						p2Count += 1
			except:
				pass
		return p1Count - p2Count

class PlayerMM(GomokuPlayer):
	def __init__(self, depthLimit, isPlayerOne):
		super().__init__(depthLimit, isPlayerOne)
	
	#returns the optimal column to move in by implementing the Minimax algorithm
	def findMove(self, board):
		if board.numMoves == 0:
			return (9,9)
		return self.findMoveHlp(board, self.isPlayerOne, self.depthLimit)[1]
	
	def findMoveHlp(self, board, turn, depth): # return type (boardval,position)
		terminalVal = board.isTerminal()
		if terminalVal == 1:	 # if White wins, (-inf,none)
			return (99999999999,None)
		elif terminalVal == 2:   # if Black wins, (inf,none)
			return (-99999999999,None)
		elif terminalVal == 0:   # if tie, (0,none)
			return (0,None)
		elif depth == 0:				# if depth 0, (heuristic,None)
			return (self.heuristic(board),None)
		else:
			bestVal = None
			bestMove = None
			if turn:
				bestVal = -math.inf
				for a in board.children():
					if a != None:
						v = self.findMoveHlp(a[1], not turn, depth-1)   # set v equal to the current child's (heur,col)
						if v[0] > bestVal:  # compare if v's heur is greater than current best val
							bestVal = v[0]  # if so, update best val with the better heur
							bestMove = a[0] # also update better move with the child's column val
			else:
				bestVal = math.inf
				for a in board.children():
					if a != None:
						v = self.findMoveHlp(a[1], not turn, depth-1)   # set v equal to the current child's (heur,col)
						if v[0] < bestVal:  # compare if v's heur is less than current best val
							bestVal = v[0]  # if so, update best val with the better heur
							bestMove = a[0] # also update better move with the child's column val
			return (bestVal,bestMove)

class PlayerAB(GomokuPlayer):

	def __init__(self, depthLimit, isPlayerOne):
		super().__init__(depthLimit, isPlayerOne)

	#returns the optimal column to move in by implementing the Alpha-Beta algorithm
	def findMove(self, board):
		if board.numMoves == 0:
			return (9,9)
		return self.findMoveHlp(board, self.isPlayerOne, self.depthLimit, -math.inf, math.inf)[1]
	
	def findMoveHlp(self, board, turn, depth, alpha, beta): # return type (boardval,position)
		terminalVal = board.isTerminal()
		if terminalVal == 1:	 # if White wins, (-inf,none)
			return (99999999999,None)
		elif terminalVal == 2:   # if Black wins, (inf,none)
			return (-99999999999,None)
		elif terminalVal == 0:   # if tie, (0,none)
			return (0,None)
		elif depth == 0:			# if depth 0, (heuristic,None)
			return (self.heuristic(board),None)
		else:
			bestVal = None
			bestMove = None
			if turn:
				bestVal = -math.inf
				for a in board.children():
					if a != None:
						v = self.findMoveHlp(a[1], not turn, depth-1, alpha, beta)   # set v equal to the current child's (heur,col)
						if v[0] > bestVal:  # compare if v's heur is greater than current best val
							bestVal = v[0]  # if so, update best val with the better heur
							bestMove = a[0] # also update better move with the child's column val
						alpha = max(alpha,bestVal)
						if alpha >= beta:
							break
			else:
				bestVal = math.inf
				for a in board.children():
					if a != None:
						v = self.findMoveHlp(a[1], not turn, depth-1, alpha, beta)   # set v equal to the current child's (heur,col)
						if v[0] < bestVal:  # compare if v's heur is less than current best val
							bestVal = v[0]  # if so, update best val with the better heur
							bestMove = a[0] # also update better move with the child's column val
						beta = min(beta,bestVal)
						if alpha >= beta:
							break
			return (bestVal,bestMove)

class PlayerABDummy(GomokuPlayer):

	def __init__(self, depthLimit, isPlayerOne):
		super().__init__(depthLimit, isPlayerOne)

	#returns the optimal column to move in by implementing the Alpha-Beta algorithm
	def findMove(self, board):
		if board.numMoves == 0:
			return (9,9)
		return self.findMoveHlp(board, self.isPlayerOne, self.depthLimit, -math.inf, math.inf)[1]
	
	def findMoveHlp(self, board, turn, depth, alpha, beta): # return type (boardval,position)
		terminalVal = board.isTerminal()
		if terminalVal == 1:	 # if White wins, (-inf,none)
			return (99999999999,None)
		elif terminalVal == 2:   # if Black wins, (inf,none)
			return (-99999999999,None)
		elif terminalVal == 0:   # if tie, (0,none)
			return (0,None)
		elif depth == 0:			# if depth 0, (heuristic,None)
			return (self.dummyHeur(board),None)
		else:
			bestVal = None
			bestMove = None
			if turn:
				bestVal = -math.inf
				for a in board.children():
					if a != None:
						v = self.findMoveHlp(a[1], not turn, depth-1, alpha, beta)   # set v equal to the current child's (heur,col)
						if v[0] > bestVal:  # compare if v's heur is greater than current best val
							bestVal = v[0]  # if so, update best val with the better heur
							bestMove = a[0] # also update better move with the child's column val
						alpha = max(alpha,bestVal)
						if alpha >= beta:
							break
			else:
				bestVal = math.inf
				for a in board.children():
					if a != None:
						v = self.findMoveHlp(a[1], not turn, depth-1, alpha, beta)   # set v equal to the current child's (heur,col)
						if v[0] < bestVal:  # compare if v's heur is less than current best val
							bestVal = v[0]  # if so, update best val with the better heur
							bestMove = a[0] # also update better move with the child's column val
						beta = min(beta,bestVal)
						if alpha >= beta:
							break
			return (bestVal,bestMove)

class PlayerNN(GomokuPlayer):
	
	def __init__(self, depthLimit, isPlayerOne):
		super().__init__(depthLimit, isPlayerOne)

	#returns the optimal column to move in by implementing the Alpha-Beta algorithm
	def findMove(self, board):
		if board.numMoves == 0:
			return (9,9)
		return self.findMoveHlp(board, self.isPlayerOne, self.depthLimit, -math.inf, math.inf)[1]
	
	def findMoveHlp(self, board, turn, depth, alpha, beta): # return type (boardval,position)
		terminalVal = board.isTerminal()
		if terminalVal == 1:	 # if White wins, (-inf,none)
			return (99999999999,None)
		elif terminalVal == 2:   # if Black wins, (inf,none)
			return (-99999999999,None)
		elif terminalVal == 0:   # if tie, (0,none)
			return (0,None)
		elif depth == 0:			# if depth 0, (heuristic,None)
			return (self.heuristicNN(board),None)
		else:
			bestVal = None
			bestMove = None
			if turn:
				bestVal = -math.inf
				for a in board.children():
					if a != None:
						v = self.findMoveHlp(a[1], not turn, depth-1, alpha, beta)   # set v equal to the current child's (heur,col)
						if v[0] > bestVal:  # compare if v's heur is greater than current best val
							bestVal = v[0]  # if so, update best val with the better heur
							bestMove = a[0] # also update better move with the child's column val
						alpha = max(alpha,bestVal)
						if alpha >= beta:
							break
			else:
				bestVal = math.inf
				for a in board.children():
					if a != None:
						v = self.findMoveHlp(a[1], not turn, depth-1, alpha, beta)   # set v equal to the current child's (heur,col)
						if v[0] < bestVal:  # compare if v's heur is less than current best val
							bestVal = v[0]  # if so, update best val with the better heur
							bestMove = a[0] # also update better move with the child's column val
						beta = min(beta,bestVal)
						if alpha >= beta:
							break
			return (bestVal,bestMove)

class PlayerNN_old(GomokuPlayer):
	
	def __init__(self, depthLimit, isPlayerOne):
		super().__init__(depthLimit, isPlayerOne)

	#returns the optimal column to move in by implementing the Alpha-Beta algorithm
	def findMove(self, board):
		if board.numMoves == 0:
			return (9,9)
		return self.findMoveHlp(board, self.isPlayerOne, self.depthLimit, -math.inf, math.inf)[1]
	
	def findMoveHlp(self, board, turn, depth, alpha, beta): # return type (boardval,position)
		terminalVal = board.isTerminal()
		if terminalVal == 1:	 # if White wins, (-inf,none)
			return (99999999999,None)
		elif terminalVal == 2:   # if Black wins, (inf,none)
			return (-99999999999,None)
		elif terminalVal == 0:   # if tie, (0,none)
			return (0,None)
		elif depth == 0:			# if depth 0, (heuristic,None)
			return (self.heuristicNN_old(board),None)
		else:
			bestVal = None
			bestMove = None
			if turn:
				bestVal = -math.inf
				for a in board.children():
					if a != None:
						v = self.findMoveHlp(a[1], not turn, depth-1, alpha, beta)   # set v equal to the current child's (heur,col)
						if v[0] > bestVal:  # compare if v's heur is greater than current best val
							bestVal = v[0]  # if so, update best val with the better heur
							bestMove = a[0] # also update better move with the child's column val
						alpha = max(alpha,bestVal)
						if alpha >= beta:
							break
			else:
				bestVal = math.inf
				for a in board.children():
					if a != None:
						v = self.findMoveHlp(a[1], not turn, depth-1, alpha, beta)   # set v equal to the current child's (heur,col)
						if v[0] < bestVal:  # compare if v's heur is less than current best val
							bestVal = v[0]  # if so, update best val with the better heur
							bestMove = a[0] # also update better move with the child's column val
						beta = min(beta,bestVal)
						if alpha >= beta:
							break
			return (bestVal,bestMove)
