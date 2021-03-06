import chess_board as cb
from random import randint
from time import time
import numpy as np
import ast


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
	with open('Games\\game_library.txt', 'r+') as file:
		games = file.read()
	games = ast.literal_eval(games)
	if not games.keys():
		key = 1
	else:
		key = max(games.keys()) + 1
	#bob = load_model('Models\\bob.h5')
	walt = load_model('Models\\walt.h5')
	epochs = 1000
	results = []
	white_wins = 0
	black_wins = 0
	stalemates = 0
	for i in range(epochs):
		print "--------------------NEW GAME-------------------_  " + str(i)
		print "White wins: " + str(white_wins)
		print  "Black wins: " + str(black_wins)
		print "Stalemates: " + str(stalemates)
		beginning = time()
		board = cb.Board()
		board.newBoard()
		gameOver = False
		winner = ""
		start = time()
		i = 1
		white_predictions = {}
		black_predictions = {}
		show_predictions = randint(1,40)
		while not gameOver:
			#exploration = randint(1,6)	
			#print "EXPLORATION: "
			white_moves = board.legalMoves()
			white_scores = []
			board_to_nn = []
			for move in white_moves:
				board.makeMove(move)
				if len(board_to_nn) == 0:
					board_to_nn = (np.reshape(board.board,(-1,64,1))+6.0)/12.0
				else:
					board_to_nn = np.vstack((board_to_nn, (np.reshape(board.board,(-1,64,1))+6.0)/12.0))
				board.undoMove()
			#if len(white_scores) > 9:
			#	white_scores_sorted = np.sort(white_scores)
			#	random_value = white_scores_sorted[-1*exploration]
			#	board.makeMove(white_moves[np.where(white_scores == random_value)[0][0]])
			#else:
			nn_prediction = walt.predict(board_to_nn)
			board.makeMove(white_moves[np.argmax(nn_prediction)])
			gameOver = board.gameOver()
			if gameOver != False:
				winner = gameOver
				break
			black_moves = board.legalMoves()
			#black_scores = []
			#for move in black_moves:
		#		board.makeMove(move)
			#	board_to_nn = (np.reshape(board.board,(-1,64,1))+6.0)/12.0
			#	if str(board_to_nn) in black_predictions.keys():
			#		black_scores.append(black_predictions[str(board_to_nn)])
			#	else:
			#		nn_prediction = bob.predict(board_to_nn)
			#		black_scores.append(nn_prediction)
			#		black_predictions[str(board_to_nn)] = nn_prediction
			#	board.undoMove()
			#if len(black_scores) > 9:
			#	black_scores_sorted = np.sort(black_scores)
			#	random_value = black_scores_sorted[-1*exploration]
			#	board.makeMove(black_moves[np.where(black_scores == random_value)[0][0]])
			#else:
			black_move = black_moves[randint(0, len(black_moves)-1)]
			board.makeMove(black_move)
			#if i == show_predictions:
			#	print black_scores
			#	print black_moves
			gameOver = board.gameOver()
			if gameOver != False:
				winner = gameOver
				break
			i += 1
		print time() - start
		print nn_prediction
		print np.argmax(nn_prediction)
		start = time()
		if winner == "white" or winner == "black":
			board.moveHistory[-1] = board.moveHistory[-1].replace('+','#')
		games[key] = board.moveHistory
		games[key] = games.key.append(winner)
		key += 1

		move_history = board.moveHistory
		print move_history
		board_configuration = board.board
		#print board_configuration
		board.showBoard()
		print winner
		results.append(winner)
		print start - beginning
		print "Game over! Training..."
		if winner == "white":
			walt_reward = 1.0
			bob_reward = -1.0
			white_wins += 1
		elif winner == "black":
			walt_reward = -1.0
			bob_reward = 1.0		
			black_wins += 1
		elif winner == "stalemate":
			stalemates += 1
		else:
			walt_reward = -0.1
			bob_reward = 0.1
		train_w_array = [((x.ravel() + 6.0)/12.0).reshape(-1,64,1) for x in board.boardHistory[1::2]]
		train_w = np.vstack(train_w_array)
		train_w_rewards = np.array([])
		for i in range(len(board.boardHistory[1::2]), 0, -1):
			train_w_rewards = np.append(train_w_rewards, 0.5 + 0.5*walt_reward/i)
		print train_w_rewards
		#earlystop = EarlyStopping(monitor='loss', min_delta=0.01, patience=5, verbose=1, mode='auto')
		#callbacks_list = [earlystop]
		#callbacks=callbacks_list,
		if winner == "black" or winner == "white":
			walt.fit(train_w,train_w_rewards, batch_size=4, epochs=12, verbose=1)
		else:
			walt.fit(train_w,train_w_rewards, batch_size=4, epochs=4, verbose=1)
		print results
		#train_b_array = [((x.ravel() + 6.0)/12.0).reshape(-1,64,1) for x in board.boardHistory[1::2]]
		#train_b = np.vstack(train_b_array)
		#train_b_rewards = np.array([])
		#for i in range(len(board.boardHistory[1::2]), 0, -1):
	#		train_b_rewards = np.append(train_b_rewards, 0.5 + 0.5*bob_reward/i)
		#print train_b_rewards
		#earlystop = EarlyStopping(monitor='loss', min_delta=0.01, patience=5, verbose=1, mode='auto')
		#callbacks_list = [earlystop]
		#callbacks=callbacks_list,
		#bob.fit(train_b,train_b_rewards, batch_size=3, epochs=6, verbose=1)




	with open('Games\\game_library.txt', 'w+') as file:
		file.write(str(games))

	#bob.save('Models\\bob.h5')
	walt.save('Models\\walt.h5')

	print results

if __name__ == "__main__":
	main()