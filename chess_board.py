import numpy as np



class Board:
	def __init__(self):
		self.newBoard()
		self.sideToMove = "white"
		self.moveHistory = []
		self.boardHistory = []
		self.moves = []
		self.pawns = ['a','b','c','d','e','f','g','h']
		self.pieces = ['','','N','B','R','Q','K']


	def newBoard(self):
		#white pieces: pawn 1, knight 2, bishop 3, rook 4, queen 5, king 6
		#minus values for black
		board = np.zeros([8,8])
		board[0] = np.array([4,2,3,5,6,3,2,4])
		board[1] = np.array([1,1,1,1,1,1,1,1])
		board[6] = -1*board[1]
		board[7] = -1*board[0]
		self.board = board
		self.coordinates = np.array([['a1','b1','c1','d1','e1','f1','g1','h1'],
									['a2','b2','c2','d2','e2','f2','g2','h2'],
									['a3','b3','c3','d3','e3','f3','g3','h3'],
									['a4','b4','c4','d4','e4','f4','g4','h4'],
									['a5','b5','c5','d5','e5','f5','g5','h5'],
									['a6','b6','c6','d6','e6','f6','g6','h6'],
									['a7','b7','c7','d7','e7','f7','g7','h7'],
									['a8','b8','c8','d8','e8','f8','g8','h8']])
		

	def showBoard(self):
		print(np.flip(self.board,axis=0))
		#print(np.flip(self.coordinates,axis=0))
		print(self.sideToMove + " to move")
		print(self.moveHistory)
		

	def legalMoves(self):
		#Returns list of all legal moves for the side who's turn it is
		sideToMove = self.sideToMove
		moves = []
		legal_moves = []
		print(sideToMove)
		if sideToMove == "white":
			#Pawns
			for i in range(8):
				for j in range(8):
					if self.board[i][j] == 1: #White Pawn
						#One square forward
						if i < 7:
							if self.board[i+1][j] == 0: #and not check
								moves.append(self.pawns[j]+str(i+2))
						if i == 1:
							#Two squares forward
							if self.board[i+1][j] == 0 and self.board[i+2][j] == 0: #and not check
								moves.append(self.pawns[j]+str(i+3))
						#Taking pawns
						if j == 0:
							if self.board[i+1][j+1] == -1: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j+1] + str(i+2))
							if self.board[i][j+1] == -1 and self.moveHistory[-1] == self.pawns[j+1] + str(i+1): #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j+1] + str(i+2) + 'e.p.')
						if j == 7:
							if self.board[i+1][j-1] == -1: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j-1] + str(i+2))
							if self.board[i][j-1] == -1 and self.moveHistory[-1] == self.pawns[j-1] + str(i+1): #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j-1] + str(i+2) + 'e.p.')
						if 0 < j < 7:
							if self.board[i+1][j+1] == -1: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j+1] + str(i+2))	
							if self.board[i+1][j-1] == -1: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j-1] + str(i+2))	
							if self.board[i][j+1] == -1 and self.moveHistory[-1] == self.pawns[j+1] + str(i+1): #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j+1] + str(i+2) + 'e.p.')
							if self.board[i][j-1] == -1 and self.moveHistory[-1] == self.pawns[j-1] + str(i+1): #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j-1] + str(i+2) + 'e.p.')
					if self.board[i][j] == 2: #White Knight:
						knightMoves = []
						#print("White knight moves")
						for l in (-2,-1,1,2):
							for m in (-2,-1,1,2):
								if abs(l) != abs(m) and 0 <= i + l <= 7 and 0 <= j + m <= 7:#Move is not to outside board
									if self.board[i+l][j+m] == 0:#Not taking anything
										knightMoves.append('N' + self.coordinates[i][j] + self.coordinates[i+l][j+m])
									elif self.board[i+l][j+m]  < 0:#Taking pawn
										knightMoves.append('N' + self.coordinates[i][j] + 'x' + self.coordinates[i+l][j+m])
						moves = moves + knightMoves
			for move in moves:
				self.makeMove(move,False)
				if "white" not in self.isCheck():
					legal_moves.append(move)
				else:
					print move
				self.undoMove()

		else:#Black to move
			#Pawns
			print("Black to move")
			for i in range(8):
				for j in range(8):
					if self.board[i][j] == -1:#Black pawn
						#One square forward
						if i > 0:
							if self.board[i-1][j] == 0: #and not check
								moves.append(self.pawns[j]+str(i))
						if i == 6:
							#Two squares forward
							if self.board[i-1][j] == 0 and self.board[i-2][j] == 0: #and not check
								moves.append(self.pawns[j]+str(i-1))
						#Taking pawns
						if j == 0:
							if self.board[i-1][j+1] == 1: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j+1] + str(i))
							if self.board[i][j+1] == 1 and self.moveHistory[-1] == self.pawns[j+1] + str(i+1): #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j+1] + str(i) + 'e.p.')
						if j == 7:
							if self.board[i-1][j-1] == 1: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j-1] + str(i))
							if self.board[i][j-1] == 1 and self.moveHistory[-1] == self.pawns[j-1] + str(i+1): #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j-1] + str(i) + 'e.p.')
						if 0 < j < 7:
							if self.board[i-1][j+1] == 1: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j+1] + str(i))	
							if self.board[i-1][j-1] == 1: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j-1] + str(i))	
							if self.board[i][j+1] == 1 and self.moveHistory[-1] == self.pawns[j+1] + str(i+1): #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j+1] + str(i) + 'e.p.')
							if self.board[i][j-1] == 1 and self.moveHistory[-1] == self.pawns[j-1] + str(i+1): #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j-1] + str(i) + 'e.p.')	
					if self.board[i][j] == -2: #Black Knight:
						knightMoves = []
						#print("Black knight moves")
						for l in (-2,-1,1,2):
							for m in (-2,-1,1,2):
								if abs(l) != abs(m) and 0 <= i + l <= 7 and 0 <= j + m <= 7:#Move is not to outside board
									if self.board[i+l][j+m] == 0:#Not taking anything
										knightMoves.append('N' + self.coordinates[i][j] + self.coordinates[i+l][j+m])
									elif self.board[i+l][j+m]  > 0:#Taking pawn
										knightMoves.append('N' + self.coordinates[i][j] + 'x' + self.coordinates[i+l][j+m])
						moves = moves + knightMoves	
			for move in moves:
				self.makeMove(move,False)
				if "black" not in self.isCheck():
					legal_moves.append(move)
				else:
					print move
				self.undoMove()	
		print(legal_moves)
		self.moves = legal_moves
		return legal_moves

	def getBoardConfiguration(self, board):
		return np.copy(board)




	def makeMove(self, move,checkMoves=True):
		self.boardHistory.append(self.getBoardConfiguration(self.board))
		color = self.sideToMove
		if color == 'white':
			color = 1
		else:
			color = -1
		if not self.moves and checkMoves:
			self.moves = self.legalMoves()
		if move not in self.moves and checkMoves:
			print("Illegal move!")
			return "Illegal move"
		#Pawns
		if move[:1] in self.pawns and 'x' not in move:
			column = self.pawns.index(move[:1])
			#print(color)
			#print(column)
			row = int(move[1:]) - 1
			#print(row)
			self.board[row][column] = color
			if self.board[row - color][column] == color:
				self.board[row - color][column] = 0
			else:
				self.board[row - 2 * color][column] = 0
		if move[:1] in self.pawns and 'x' in move:
			target = move[2:4]
			#print(target)
			target = zip(*np.where(self.coordinates == target))[0]
			row = target[0]
			column = target[1]
			self.board[row][column] = color
			if 'e.p.' in move:
				self.board[row - color][column] = 0
			column = self.pawns.index(move[:1])
			row = target[0] - color
			self.board[row][column] = 0	
		if move[:1] == 'N':#Knight move
			target = move[-2:]
			target = zip(*np.where(self.coordinates == target))[0]
			row = target[0]
			column = target[1]
			self.board[row][column] = color*2
			target = move[1:3]
			target = zip(*np.where(self.coordinates == target))[0]
			row = target[0]
			column = target[1]
			self.board[row][column] = 0

		self.moves = []
		self.moveHistory.append(move)
		if color == 1:
			self.sideToMove = 'black'
		else:
			self.sideToMove = 'white'

	def undoMove(self):
		if len(self.moveHistory) == 0:
			print("No moves have been made!")
			return 0
		#print(self.board == self.boardHistory[-1])
		self.board = self.boardHistory[-1]
		self.boardHistory = self.boardHistory[:-1]
		self.moveHistory = self.moveHistory[:-1]
		if self.sideToMove == "white":
			self.sideToMove = "black"
		else:
			self.sideToMove = "white"

	def isCheck(self):
		#Returns "white" if white is in check, "black" if black is in check
		#Otherwise returns Empty list
		#First check if white king is in check
		checks = []
		diagonalCheckGivers = [3,5,6]#Bishop,queen and king
		verticalCheckGivers = [4,5,6]#Rook, queen and king

		whiteKing = zip(*np.where(self.board == 6))[0]
		#print whiteKing
		kingColumn = self.board[:,whiteKing[1]]
		kingRow = self.board[whiteKing[0]]
		kingRightDiagonal = np.array([])
		row = whiteKing[0]
		column = whiteKing[1]
		while row >= 0 and column >= 0:
			row -= 1
			column -= 1
		row += 1
		column += 1
		while row < 8 and column < 8:
			if self.board[row][column] != 0:
				kingRightDiagonal = np.append(kingRightDiagonal, self.board[row][column])
			row += 1
			column += 1
		kingLeftDiagonal = np.array([])
		row = whiteKing[0]
		column = whiteKing[1]
		while row >= 0 and column < 8:
			row -= 1
			column += 1
		row += 1
		column -= 1
		while row < 8 and column >= 0:
			if self.board[row][column] != 0:
				kingLeftDiagonal = np.append(kingLeftDiagonal, self.board[row][column])
			row += 1
			column -= 1
		#print kingColumn
		#print kingRow
		#print kingRightDiagonal
		#print kingLeftDiagonal

		for row in [kingColumn,kingRow]:
			row = np.insert(row,0,0)
			row = np.append(row,0)
			kingIndex = np.where(row == 6)[0][0]
			try:
				in_front = row[kingIndex + 1]
			except:
				in_front = 0
			if -1*in_front in verticalCheckGivers:
				print("check from front")
				checks.append("white")
			try:
				in_back = row[kingIndex - 1]
			except:
				in_back = 0
			if -1*in_back in verticalCheckGivers:
				checks.append("white")
			
		for row in [kingLeftDiagonal,kingRightDiagonal]:
			row = np.insert(row,0,0)
			row = np.append(row,0)
			kingIndex = np.where(row == 6)[0][0]
			try:
				in_front = row[kingIndex + 1]
			except:
				in_front = 0
			if -1*in_front in verticalCheckGivers:
				checks.append("white")
			try:
				in_back = row[kingIndex - 1]
			except:
				in_back = 0
			if -1*in_back in verticalCheckGivers:
				checks.append("white")
			if whiteKing[0] < 7:
				if self.board[whiteKing[0] + 1][whiteKing[1] + 1] == -1 or self.board[whiteKing[0] + 1][whiteKing[1] - 1] == -1:
					checks.append("white")
		
		#Knights
		for l in (-2,-1,1,2):
			for m in (-2,-1,1,2):
				if abs(l) != abs(m) and 0 <= whiteKing[0] + l <= 7 and 0 <= whiteKing[1] + m <= 7:
					if self.board[whiteKing[0] + l][whiteKing[1] + m] == -2:
						checks.append("white")
		
		blackKing = zip(*np.where(self.board == -6))[0]
		#print blackKing
		kingColumn = self.board[:,blackKing[1]]
		kingRow = self.board[blackKing[0]]
		kingRightDiagonal = np.array([])
		row = blackKing[0]
		column = blackKing[1]
		while row >= 0 and column >= 0:
			row -= 1
			column -= 1
		row += 1
		column += 1
		while row < 8 and column < 8:
			if self.board[row][column] != 0:
				kingRightDiagonal = np.append(kingRightDiagonal, self.board[row][column])
			row += 1
			column += 1
		kingLeftDiagonal = np.array([])
		row = blackKing[0]
		column = blackKing[1]
		while row >= 0 and column < 8:
			row -= 1
			column += 1
		row += 1
		column -= 1
		while row < 8 and column >= 0:
			if self.board[row][column] != 0:
				kingLeftDiagonal = np.append(kingLeftDiagonal, self.board[row][column])
			row += 1
			column -= 1
		#print kingColumn
		#print kingRow
		#print kingRightDiagonal
		#print kingLeftDiagonal
		for row in [kingColumn,kingRow]:
			row = np.insert(row,0,0)
			row = np.append(row,0)
			kingIndex = np.where(row == -6)[0][0]
			try:
				in_front = row[kingIndex + 1]
			except:
				in_front = 0
			if in_front in verticalCheckGivers:
				checks.append("black")
			try:
				in_back = row[kingIndex - 1]
			except:
				in_back = 0
			if in_back in verticalCheckGivers:
				checks.append("black")
			
		for row in [kingLeftDiagonal,kingRightDiagonal]:
			row = np.insert(row,0,0)
			row = np.append(row,0)
			kingIndex = np.where(row == -6)[0][0]
			try:
				in_front = row[kingIndex + 1]
			except:
				in_front = 0
			if in_front in verticalCheckGivers:
				checks.append("black")
			try:
				in_back = row[kingIndex - 1]
			except:
				in_back = 0
			if in_back in verticalCheckGivers:
				checks.append("black")
			if blackKing[0] > 0:
				if self.board[blackKing[0] - 1][blackKing[1] + 1] == 1 or self.board[blackKing[0] - 1][blackKing[1] - 1] == 1:
					checks.append("black")
			
		#Knights
		for l in (-2,-1,1,2):
			for m in (-2,-1,1,2):
				if abs(l) != abs(m) and 0 <= blackKing[0] + l <= 7 and 0 <= blackKing[1] + m <= 7:
					if self.board[blackKing[0] + l][blackKing[1] + m] == 2:
						checks.append("black")
		print checks
		return checks


x = Board()
x.showBoard()
x.legalMoves()
#x.isCheck()
x.makeMove('Nb1a3')
x.makeMove('a6')

x.makeMove('Na3b5')
x.makeMove('a5')
x.showBoard()
x.isCheck()
x.legalMoves()
'''
x.undoMove()
x.makeMove('a4')
x.showBoard()
x.legalMoves()
x.makeMove('a6')
x.showBoard()
x.legalMoves()
x.makeMove('a5')
x.showBoard()
x.legalMoves()
x.makeMove('b5')
x.showBoard()
x.legalMoves()
x.makeMove('axb6e.p.')
x.showBoard()
x.legalMoves()
x.makeMove('Ng8h6')
x.showBoard()
x.legalMoves()
x.makeMove('c3')
x.showBoard()
x.legalMoves()
x.makeMove('a5')
x.showBoard()
x.legalMoves()
print(x.moveHistory)
x.isCheck()
#print(x.boardHistory)
'''