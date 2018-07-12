import chess_board as cb
from random import randint
from time import time
import numpy as np
import ast
import sys


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
	with open('Games\\generation_3.txt', 'r+') as file:
		games = file.read()
	games = ast.literal_eval(games)
	if not games.keys():
		key = 1
	else:
		key = max(games.keys()) + 1
	#bob = load_model('Models\\bob.h5')
	walt = load_model('Models\\walt_gen_1_child_0.h5')
	bob = load_model('Models\\bob_gen_2_child_0.h5')

	print "--------------------EVOLVING----------------------"

	evolving = sys.argv[1]
	results = []
	while evolving not in results:
		results = []
		if evolving == 'white':
			walt_child_1 = load_model('Models\\walt_gen_1_child_0.h5')
			weights = walt_child_1.get_weights()
			for i in range(len(weights)):
				if len(weights[i].shape) == 1:
					modification = 0.001*np.random.randn(len(weights[i]))
					weights[i] += modification
				else:
					for j in range(len(weights[i])):
						if len(weights[i][j].shape) == 1:
							modification = 0.001*np.random.randn(len(weights[i][j]))
							weights[i][j] += modification
						else:
							for k in range(len(weights[i][j])):
								if len(weights[i][j][k].shape) == 1:
									modification = 0.001*np.random.randn(len(weights[i][j][k]))
									weights[i][j][k] += modification						
			walt_child_1.set_weights(weights)

			walt_child_2 = load_model('Models\\walt_gen_1_child_0.h5')
			weights = walt_child_2.get_weights()
			for i in range(len(weights)):
				if len(weights[i].shape) == 1:
					modification = 0.005*np.random.randn(len(weights[i]))
					weights[i] += modification
				else:
					for j in range(len(weights[i])):
						if len(weights[i][j].shape) == 1:
							modification = 0.005*np.random.randn(len(weights[i][j]))
							weights[i][j] += modification
						else:
							for k in range(len(weights[i][j])):
								if len(weights[i][j][k].shape) == 1:
									modification = 0.005*np.random.randn(len(weights[i][j][k]))
									weights[i][j][k] += modification						
			walt_child_2.set_weights(weights)

			walt_child_3 = load_model('Models\\walt_gen_1_child_0.h5')
			weights = walt_child_3.get_weights()
			for i in range(len(weights)):
				if len(weights[i].shape) == 1:
					modification = 0.01*np.random.randn(len(weights[i]))
					weights[i] += modification
				else:
					for j in range(len(weights[i])):
						if len(weights[i][j].shape) == 1:
							modification = 0.01*np.random.randn(len(weights[i][j]))
							weights[i][j] += modification
						else:
							for k in range(len(weights[i][j])):
								if len(weights[i][j][k].shape) == 1:
									modification = 0.01*np.random.randn(len(weights[i][j][k]))
									weights[i][j][k] += modification						
			walt_child_3.set_weights(weights)

			walt_child_4 = load_model('Models\\walt_gen_1_child_0.h5')
			weights = walt_child_4.get_weights()
			for i in range(len(weights)):
				if len(weights[i].shape) == 1:
					modification = 0.05*np.random.randn(len(weights[i]))
					weights[i] += modification
				else:
					for j in range(len(weights[i])):
						if len(weights[i][j].shape) == 1:
							modification = 0.05*np.random.randn(len(weights[i][j]))
							weights[i][j] += modification
						else:
							for k in range(len(weights[i][j])):
								if len(weights[i][j][k].shape) == 1:
									modification = 0.05*np.random.randn(len(weights[i][j][k]))
									weights[i][j][k] += modification						
			walt_child_4.set_weights(weights)

		elif evolving == 'black':
			bob_child_1 = load_model('Models\\bob_gen_2_child_0.h5')
			weights = bob_child_1.get_weights()
			for i in range(len(weights)):
				if len(weights[i].shape) == 1:
					modification = 0.001*np.random.randn(len(weights[i]))
					weights[i] += modification
				else:
					for j in range(len(weights[i])):
						if len(weights[i][j].shape) == 1:
							modification = 0.001*np.random.randn(len(weights[i][j]))
							weights[i][j] += modification
						else:
							for k in range(len(weights[i][j])):
								if len(weights[i][j][k].shape) == 1:
									modification = 0.001*np.random.randn(len(weights[i][j][k]))
									weights[i][j][k] += modification						
			bob_child_1.set_weights(weights)

			bob_child_2 = load_model('Models\\bob_gen_2_child_0.h5')
			weights = bob_child_2.get_weights()
			for i in range(len(weights)):
				if len(weights[i].shape) == 1:
					modification = 0.005*np.random.randn(len(weights[i]))
					weights[i] += modification
				else:
					for j in range(len(weights[i])):
						if len(weights[i][j].shape) == 1:
							modification = 0.005*np.random.randn(len(weights[i][j]))
							weights[i][j] += modification
						else:
							for k in range(len(weights[i][j])):
								if len(weights[i][j][k].shape) == 1:
									modification = 0.005*np.random.randn(len(weights[i][j][k]))
									weights[i][j][k] += modification						
			bob_child_2.set_weights(weights)

			bob_child_3 = load_model('Models\\bob_gen_2_child_0.h5')
			weights = bob_child_3.get_weights()
			for i in range(len(weights)):
				if len(weights[i].shape) == 1:
					modification = 0.01*np.random.randn(len(weights[i]))
					weights[i] += modification
				else:
					for j in range(len(weights[i])):
						if len(weights[i][j].shape) == 1:
							modification = 0.01*np.random.randn(len(weights[i][j]))
							weights[i][j] += modification
						else:
							for k in range(len(weights[i][j])):
								if len(weights[i][j][k].shape) == 1:
									modification = 0.01*np.random.randn(len(weights[i][j][k]))
									weights[i][j][k] += modification						
			bob_child_3.set_weights(weights)

			bob_child_4 = load_model('Models\\bob_gen_2_child_0.h5')
			weights = bob_child_4.get_weights()
			for i in range(len(weights)):
				if len(weights[i].shape) == 1:
					modification = 0.05*np.random.randn(len(weights[i]))
					weights[i] += modification
				else:
					for j in range(len(weights[i])):
						if len(weights[i][j].shape) == 1:
							modification = 0.05*np.random.randn(len(weights[i][j]))
							weights[i][j] += modification
						else:
							for k in range(len(weights[i][j])):
								if len(weights[i][j][k].shape) == 1:
									modification = 0.05*np.random.randn(len(weights[i][j][k]))
									weights[i][j][k] += modification						
			bob_child_4.set_weights(weights)
		
		if evolving == 'white':
			childs = [walt_child_1,walt_child_2,walt_child_3,walt_child_4]
		elif evolving == 'black':
			childs = [bob_child_1,bob_child_2,bob_child_3,bob_child_4]
		for child in childs:
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
				if evolving == 'white':
					nn_prediction = child.predict(board_to_nn)
				else:
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
				if evolving == 'black':
					nn_prediction = child.predict(board_to_nn)
				else:
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
			games[key] = board.moveHistory
			key += 1

			move_history = board.moveHistory
			print move_history
			board_configuration = board.board
			#print board_configuration
			board.showBoard()
			print winner
			results.append(winner)
			print start - beginning
			print "Game over!"


	with open('Games\\generation_3.txt', 'w+') as file:
		file.write(str(games))

	#bob.save('Models\\bob.h5')
	for i in range(len(results)):
		if results[i] == 'white':
			childs[i].save(r'Models\walt_gen_3_child_' + str(i) + '.h5')

if __name__ == "__main__":
	main()