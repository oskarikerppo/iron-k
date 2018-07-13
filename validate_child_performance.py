import chess_board as cb
from random import randint
from time import time
import numpy as np
import ast
from os import listdir
from os.path import isfile, join

import keras
from keras.models import Sequential, Input, Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv1D, MaxPooling1D
from keras.layers.normalization import BatchNormalization
from keras.models import load_model
from keras.callbacks import EarlyStopping



#todo
#until game starts to get won and models learn do random moves most of the time
#early stopping?
#END OF GAME CONDITIONS
#SAVE PREDICTED VALUES FOR LATER USE
#Show predictions of moves to show that they are changing

def main():
	engine_files = [f for f in listdir("Models") if isfile(join("Models", f))]
	engine_files = [x for x in engine_files if 'gen' in x and 'child' in x]
	engine_files.sort(key=lambda x: int(x.split('_')[2]),reverse=True)
	bob_files = [x for x in engine_files if 'bob' in x]
	walt_files = [x for x in engine_files if 'walt' in x]
	current_walt = load_model('Models\\' + walt_files[0])
	current_bob = load_model('Models\\' + bob_files[0])

	bob_results = []
	walt_results = []
	for bob in bob_files:
		print "--------------------NEW GAME----------------------"
		bob = load_model('Models\\' + bob)
		beginning = time()
		board = cb.Board()
		gameOver = False
		winner = ""
		start = time()
		i = 1
		white_predictions = {}
		black_predictions = {}
		while not gameOver:
			white_moves = board.legalMoves()
			board_to_nn = []
			for move in white_moves:
				board.makeMove(move)
				if len(board_to_nn) == 0:
					board_to_nn = (np.reshape(board.board,(-1,64,1))+6.0)/12.0
				else:
					board_to_nn = np.vstack((board_to_nn, (np.reshape(board.board,(-1,64,1))+6.0)/12.0))
				board.undoMove()
			nn_prediction = current_walt.predict(board_to_nn)
			board.makeMove(white_moves[np.argmax(nn_prediction)])
			gameOver = board.gameOver()
			if gameOver != False:
				winner = gameOver
				break
			black_moves = board.legalMoves()
			board_to_nn = []
			for move in black_moves:
				board.makeMove(move)
				if len(board_to_nn) == 0:
					board_to_nn = (np.reshape(board.board,(-1,64,1))+6.0)/12.0
				else:
					board_to_nn = np.vstack((board_to_nn, (np.reshape(board.board,(-1,64,1))+6.0)/12.0))
				board.undoMove()
			nn_prediction = bob.predict(board_to_nn)
			board.makeMove(black_moves[np.argmax(nn_prediction)])
			gameOver = board.gameOver()
			if gameOver != False:
				winner = gameOver
				break
			gameOver = board.gameOver()
			if gameOver != False:
				winner = gameOver
				break
			i += 1
		print time() - start
		start = time()
		if winner == "white" or winner == "black":
			board.moveHistory[-1] = board.moveHistory[-1].replace('+','#')

		move_history = board.moveHistory
		print move_history
		board_configuration = board.board
		#print board_configuration
		board.showBoard()
		print winner
		print start - beginning
		print "Game over!"
		walt_results.append(winner)


	for walt in walt_files:
		walt = load_model('Models\\' + walt)
		print "--------------------NEW GAME----------------------"
		beginning = time()
		board = cb.Board()
		gameOver = False
		winner = ""
		start = time()
		i = 1
		white_predictions = {}
		black_predictions = {}
		while not gameOver:
			white_moves = board.legalMoves()
			board_to_nn = []
			for move in white_moves:
				board.makeMove(move)
				if len(board_to_nn) == 0:
					board_to_nn = (np.reshape(board.board,(-1,64,1))+6.0)/12.0
				else:
					board_to_nn = np.vstack((board_to_nn, (np.reshape(board.board,(-1,64,1))+6.0)/12.0))
				board.undoMove()
			nn_prediction = walt.predict(board_to_nn)
			board.makeMove(white_moves[np.argmax(nn_prediction)])
			gameOver = board.gameOver()
			if gameOver != False:
				winner = gameOver
				break
			black_moves = board.legalMoves()
			board_to_nn = []
			for move in black_moves:
				board.makeMove(move)
				if len(board_to_nn) == 0:
					board_to_nn = (np.reshape(board.board,(-1,64,1))+6.0)/12.0
				else:
					board_to_nn = np.vstack((board_to_nn, (np.reshape(board.board,(-1,64,1))+6.0)/12.0))
				board.undoMove()
			nn_prediction = current_bob.predict(board_to_nn)
			board.makeMove(black_moves[np.argmax(nn_prediction)])
			gameOver = board.gameOver()
			if gameOver != False:
				winner = gameOver
				break
			gameOver = board.gameOver()
			if gameOver != False:
				winner = gameOver
				break
			i += 1
		print time() - start
		start = time()
		if winner == "white" or winner == "black":
			board.moveHistory[-1] = board.moveHistory[-1].replace('+','#')


		move_history = board.moveHistory
		print move_history
		board_configuration = board.board
		#print board_configuration
		board.showBoard()
		print winner
		print start - beginning
		print "Game over!"
		bob_results.append(winner)

	print "Walt results: "
	print walt_results
	walt_wins = 0
	for game in walt_results:
		if game == "white":
			walt_wins += 1
	print "Walt won " + str(walt_wins) + " games!"
	print "Bob results: "
	print bob_results
	bob_wins = 0
	for game in bob_results:
		if game == "black":
			bob_wins += 1
	print "Bob won " + str(bob_wins) + " games!"


if __name__ == "__main__":
	main()