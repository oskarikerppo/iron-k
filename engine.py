import chess_board as cb
from random import randint
from time import time



beginning = time()
board = cb.Board()
board.newBoard()

gameOver = False
winner = ""
start = time()
while not gameOver:
	white_moves = board.legalMoves()
	board.makeMove(white_moves[randint(0,len(white_moves)-1)])
	gameOver = board.gameOver()
	if gameOver != False:
		winner = gameOver
		break
	black_moves = board.legalMoves()
	board.makeMove(black_moves[randint(0,len(black_moves)-1)])
	gameOver = board.gameOver()
	if gameOver != False:
		winner = gameOver
		break
	print time() - start
	start = time()


move_history = board.moveHistory
print move_history
board_configuration = board.board
#print board_configuration
board.showBoard()
print winner
print start - beginning