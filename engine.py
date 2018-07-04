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
	bob = load_model('Models\\bob.h5')
	walt = load_model('Models\\walt.h5')

	epochs = 12
	for i in range(epochs):
		beginning = time()
		board = cb.Board()
		board.newBoard()
		gameOver = False
		winner = ""
		start = time()
		while not gameOver:
			white_moves = board.legalMoves()
			white_scores = []
			for move in white_moves:
				board.makeMove(move)
				white_scores.append(walt.predict(np.reshape(board.board,(-1,64,1))))
				board.undoMove()
			board.makeMove(white_moves[np.argmax(white_scores)])
			gameOver = board.gameOver()
			if gameOver != False:
				winner = gameOver
				break
			black_moves = board.legalMoves()
			black_scores = []
			for move in black_moves:
				board.makeMove(move)
				black_scores.append(bob.predict(np.reshape(board.board,(-1,64,1))))
				board.undoMove()
			board.makeMove(black_moves[np.argmax(black_scores)])
			gameOver = board.gameOver()
			if gameOver != False:
				winner = gameOver
				break
			print time() - start
			start = time()

		games[key] = board.moveHistory
		key += 1

		move_history = board.moveHistory
		print move_history
		board_configuration = board.board
		#print board_configuration
		board.showBoard()
		print winner
		print start - beginning
		print "Game over! Training..."
		if winner == "white":
			walt_reward = 1.0
			bob_reward = -1.0
		elif winner == "black":
			walt_reward = -1.0
			bob_reward = 1.0		
		else:
			walt_reward = -0.2
			bob_reward = 0.2
		train_w_array = [x.ravel().reshape(-1,64,1) for x in board.boardHistory[::2]]
		train_w = np.vstack(train_w_array)
		train_w_rewards = np.array([])
		for i in range(len(board.boardHistory[::2]), 0, -1):
			train_w_rewards = np.append(train_w_rewards,walt_reward/i)
		#earlystop = EarlyStopping(monitor='loss', min_delta=0.01, patience=5, verbose=1, mode='auto')
		#callbacks_list = [earlystop]
		#callbacks=callbacks_list,
		walt.fit(train_w,train_w_rewards, batch_size=4, epochs=40, verbose=1)

		train_b_array = [x.ravel().reshape(-1,64,1) for x in board.boardHistory[1::2]]
		train_b = np.vstack(train_b_array)
		train_b_rewards = np.array([])
		for i in range(len(board.boardHistory[1::2]), 0, -1):
			train_b_rewards = np.append(train_b_rewards,bob_reward/i)
		#earlystop = EarlyStopping(monitor='loss', min_delta=0.01, patience=5, verbose=1, mode='auto')
		#callbacks_list = [earlystop]
		#callbacks=callbacks_list,
		bob.fit(train_b,train_b_rewards, batch_size=4, epochs=40, verbose=1)




	with open('Games\\game_library.txt', 'w+') as file:
		file.write(str(games))

	bob.save('Models\\bob.h5')
	walt.save('Models\\walt.h5')

if __name__ == "__main__":
	main()