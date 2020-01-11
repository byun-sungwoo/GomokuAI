# Gomoku Project [GomokuBoard]
# B351 - Sreekar Antharam, Daniel Byun, Andrew Chong

class GomokuBoard(object):
	HEIGHT = 19
	WIDTH = 19

	def __init__(self, orig=None, hash=None):
		if(orig):
			self.board = [list(col) for col in orig.board]
			self.numMoves = orig.numMoves
			self.lastMove = orig.lastMove
			return
		elif(hash):
			self.board = []
			self.numMoves = 0
			self.lastMove = None
			digits = []
			while hash:
				digits.append(int(hash % 3))
				hash //= 3
			col = []
			for item in digits:
				if item == 2:
					self.board.append(col)
					col = []
				else:
					col.append(item)
					self.numMoves += 1
			return
		else:
			self.board = [[None for x in range(19)] for y in range(19)]
			self.numMoves = 0
			self.lastMove = None
			return

	# Puts a piece in the appropriate position
	# (0,0) is bottom left corner
	def makeMove(self, position):
		#update board data
		piece = self.numMoves % 2
		self.lastMove = (piece, position)
		self.numMoves += 1
		self.board[position[0]][position[1]] = piece

	# Returns an X and Y range in the shape of a box, for
	# valid moves to reduce thinking time
	def childRange(self):
		minX=19
		minY=19
		maxX=0
		maxY=0
		for a in range(19):
			for b in range(19):
				if self.board[a][b] != None:
					if a > maxX:
						maxX = a
					if a < minX:
						minX = a
					if b > maxY:
						maxY = b
					if b < minY:
						minY = b
		if minX != 0:
			minX -= 1
		if minY != 0:
			minY -= 1
		if maxX != 19:
			maxX += 1
		if maxY != 19:
			maxY += 1
		return ((minX,maxX),(minY,maxY))
	
	# Generates a list of the valid children of the board
	# A child is of the form (move_to_make_child, child_object)
	def children(self):
		potential=self.childRange()
		children = []
		for i in range(potential[0][0],potential[0][1]):
			for j in range(potential[1][0],potential[1][1]):
				if self.board[i][j] == None:
					child = GomokuBoard(self)
					child.makeMove((i,j))
					children.append(((i,j), child))
		return children

	# Returns:
	#  -1 if game is not over
	#   0 if the game is a draw
	#   1 if player 1 wins
	#   2 if player 2 wins
	# for diagonal check from bottom row and build a string for the diagonals pointing to right going up (x+1,x+1) and then check the first col building a string for each one again (x+1,x+1)
	# for diagonal from left pointing right bottom row and build string (x-1,x+1) and same for right column (x-1, x+1)
	def isTerminal(self):
		rowList = ["","","","","","","","","","","","","","","","","","",""]
		colList = ["","","","","","","","","","","","","","","","","","",""]
		# ===BUILDING ROWS AND COLUMNS===
		for a in range(self.WIDTH):
			for b in range(self.HEIGHT):
				if len(self.board[a]) > b:
					if self.board[a][b] == 0:
						colList[a] += "0"
						rowList[b] += "0"
					elif self.board[a][b] == 1:
						colList[a] += "@"
						rowList[b] += "@"
					else:
						colList[a] += "_"
						rowList[b] += "_"
				else:
					colList[a] += "_"
					rowList[b] += "_"
				if "00000" in rowList[b]:
					return 1
				elif "@@@@@" in rowList[b]:
					return 2
				if "00000" in colList[a]:
					return 1
				elif "@@@@@" in colList[a]:
					return 2
		# ===BUILDING RIGHT DIAGONAL===
		for a in range(self.HEIGHT):	# building diagonal starting from row to col for right diagonal
			currentList = ""
			currentPos = (0,a)
			while(self.inRange(currentPos)):
				try:
					if self.board[currentPos[0]][currentPos[1]] == 0:
						currentList += "0"
					elif self.board[currentPos[0]][currentPos[1]] == 1:
						currentList += "@"
					else:
						currentList += "_"
					currentPos = (currentPos[0]+1,currentPos[1]+1)
				except IndexError:
					currentList += "_"
					currentPos = (currentPos[0]+1,currentPos[1]+1)
			if "00000" in currentList:
				return 1
			elif "@@@@@" in currentList:
				return 2
		for a in range(self.WIDTH):	# building diagonal currently on columns for right
			currentList = ""
			currentPos = (a,0)
			while(self.inRange(currentPos)):
				try:
					if self.board[currentPos[0]][currentPos[1]] == 0:
						currentList += "0"
					elif self.board[currentPos[0]][currentPos[1]] == 1:
						currentList += "@"
					else:
						currentList += "_"
					currentPos = (currentPos[0]+1,currentPos[1]+1)
				except IndexError:
					currentList += "_"
					currentPos = (currentPos[0]+1,currentPos[1]+1)
			if "00000" in currentList:
				return 1
			elif "@@@@@" in currentList:
				return 2
		# ===BUILDING LEFT DIAGONAL===
		for a in range(self.HEIGHT):	# building diagonal starting from row to col for left diagonal
			currentList = ""
			currentPos = (19,a)
			while(self.inRange(currentPos)):
				try:
					if self.board[currentPos[0]][currentPos[1]] == 0:
						currentList += "0"
					elif self.board[currentPos[0]][currentPos[1]] == 1:
						currentList += "@"
					else:
						currentList += "_"
					currentPos = (currentPos[0]-1,currentPos[1]+1)
				except IndexError:
					currentList += "_"
					currentPos = (currentPos[0]-1,currentPos[1]+1)
			if "00000" in currentList:
				return 1
			elif "@@@@@" in currentList:
				return 2
		for a in range(self.WIDTH):	# building diagonal currently on columns for left
			currentList = ""
			currentPos = (a,0)
			while(self.inRange(currentPos)):
				try:
					if self.board[currentPos[0]][currentPos[1]] == 0:
						currentList += "0"
					elif self.board[currentPos[0]][currentPos[1]] == 1:
						currentList += "@"
					else:
						currentList += "_"
					currentPos = (currentPos[0]-1,currentPos[1]+1)
				except IndexError:
					currentList += "_"
					currentPos = (currentPos[0]-1,currentPos[1]+1)
			if "00000" in currentList:
				return 1
			elif "@@@@@" in currentList:
				return 2
		# if we are here then no one has won yet, so check if it's a tie or still going
		if self.isFull():
			return 0
		else:
			return -1

	# checks if the position given is in the board or not
	def inRange(self,position):
		if position[0] < 19 and position[0] > -1 and position[1] < 19 and position[1] > -1:
			return True
		else:
			return False

	# Retuns a unique decimal number for each board object based on the
	# underlying data
	def hash(self):
		power = 0
		hash = 0
		for column in self.board:
			for piece in column:
				hash += piece * (3 ** power)
				power += 1
			hash += 2 * (3 ** power)
			power += 1
		return hash

	# Return true iff the game is full
	def isFull(self):
		return self.numMoves == 361

	# Prints out a visual representation of the board
	# 0 is white [0] and 1 is black [@]
	def print(self):
		print("")
		print("+" + "---+" * self.WIDTH)
		for rowNum in range(self.HEIGHT - 1, -1, -1):
			row = "|"
			for colNum in range(self.WIDTH):
				if len(self.board[colNum]) > rowNum:
					if self.board[colNum][rowNum] == 0:
						row += " " + "0" + " |"
					elif self.board[colNum][rowNum] == 1:
						row += " " + "@" + " |"
					else:
						row += "   |"
				else:
					row += "   |"
			print(row)
			print("+" + "---+" * self.WIDTH)
