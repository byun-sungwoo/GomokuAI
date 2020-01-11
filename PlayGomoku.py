# Gomoku Project [PlayGomoku]
# B351 - Sreekar Antharam, Daniel Byun, Andrew Chong

from GomokuBoard import *
from GomokuPlayer import *

class Game:
	def __init__(self, startBoard, player1, player2):
		self.startBoard = startBoard
		self.player1 = player1
		self.player2 = player2
	def simulateLocalGame(self):
		board = GomokuBoard(orig=self.startBoard)
		isPlayer1 = True
		while(True):
			if isPlayer1:
				move = self.player1.findMove(board)
			else:
				move = self.player2.findMove(board)
			board.makeMove(move)
			board.print()
			isOver = board.isTerminal()
			if isOver == 0:
				print("It is a draw!")
				break
			elif isOver == 1:
				print("Player 1 wins!")
				break
			elif isOver == 2:
				print("Player 2 wins!")
				break
			else:
				isPlayer1 = not isPlayer1

def main():
	print("main1")
	board = GomokuBoard()
	player1 = PlayerNN(2,True)
	player2 = PlayerNN_old(2,False)
	game = Game(board, player1, player2)
	game.simulateLocalGame()

if __name__ == '__main__':
	print("main")
	main()
