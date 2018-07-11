import numpy as np
from random import randint

#todo list, buglist
#en passant is bugged, must check that pawn moved two squares
#checks might be bugged

#moves and checks for queen, king, bishob and rook
#castling
#end of game conditions


#BUG !!! PAWN TAKES LAST ROW MUST PROMOTE !!!! FIXED
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
		##print(np.flip(self.coordinates,axis=0))
		print(self.sideToMove + " to move")
		print(self.moveHistory)
		

	def legalMoves(self):
		#Returns list of all legal moves for the side who's turn it is
		sideToMove = self.sideToMove
		moves = []
		legal_moves = []
		##print(sideToMove)
		if sideToMove == "white":
			#Pawns
			for i in range(8):
				for j in range(8):
					if self.board[i][j] == 0:
						continue
					elif self.board[i][j] == 1: #White Pawn
						#One square forward
						if i < 6:
							if self.board[i+1][j] == 0: #and not check
								moves.append(self.pawns[j]+str(i+2))
						if i == 1:
							#Two squares forward
							if self.board[i+1][j] == 0 and self.board[i+2][j] == 0: #and not check
								moves.append(self.pawns[j]+str(i+3))
						if i == 6 and self.board[i + 1][j] == 0:
							moves.append(self.pawns[j] + "8Q")
							moves.append(self.pawns[j] + "8R")
							moves.append(self.pawns[j] + "8N")
							moves.append(self.pawns[j] + "8B")
						#Taking pawns and pieces
						if 2 <= i + 1 <= 7 and 0 <= j + 1 <= 7 and self.board[i + 1][j + 1] < -1:
							if i == 6:
								moves.append(self.pawns[j] + 'x' + self.coordinates[i + 1][j + 1] + "Q")
								moves.append(self.pawns[j] + 'x' + self.coordinates[i + 1][j + 1] + "R")
								moves.append(self.pawns[j] + 'x' + self.coordinates[i + 1][j + 1] + "N")
								moves.append(self.pawns[j] + 'x' + self.coordinates[i + 1][j + 1] + "B")
							else:
								moves.append(self.pawns[j] + 'x' + self.coordinates[i + 1][j + 1])
						if 2 <= i + 1 <= 7 and 0 <= j - 1 <= 7 and self.board[i + 1][j - 1] < -1:
							if i == 6:
								moves.append(self.pawns[j] + 'x' + self.coordinates[i + 1][j - 1] + "Q")
								moves.append(self.pawns[j] + 'x' + self.coordinates[i + 1][j - 1] + "R")
								moves.append(self.pawns[j] + 'x' + self.coordinates[i + 1][j - 1] + "N")
								moves.append(self.pawns[j] + 'x' + self.coordinates[i + 1][j - 1] + "B")
							else:
								moves.append(self.pawns[j] + 'x' + self.coordinates[i + 1][j - 1])
						if j == 0 and i < 7:
							if self.board[i+1][j+1] == -1: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j+1] + str(i+2))
							if i == 4 and self.board[i][j+1] == -1 and self.moveHistory[-1] == self.pawns[j+1] + str(i + 1) and self.pawns[j+1] + str(i + 2) not in self.moveHistory: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j+1] + str(i + 2) + 'e.p.')
						elif j == 7 and i < 7:
							if self.board[i+1][j-1] == -1: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j-1] + str(i+2))
							if i == 4 and self.board[i][j-1] == -1 and self.moveHistory[-1] == self.pawns[j-1] + str(i + 1) and self.pawns[j-1] + str(i + 2) not in self.moveHistory: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j-1] + str(i + 2) + 'e.p.')
						elif i < 7:
							if self.board[i+1][j+1] == -1: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j+1] + str(i+2))	
							if self.board[i+1][j-1] == -1: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j-1] + str(i+2))	
							if i == 4 and self.board[i][j+1] == -1 and self.moveHistory[-1] == self.pawns[j+1] + str(i + 1) and self.pawns[j+1] + str(i + 2) not in self.moveHistory: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j+1] + str(i + 2) + 'e.p.')
							if i == 4 and self.board[i][j-1] == -1 and self.moveHistory[-1] == self.pawns[j-1] + str(i + 1) and self.pawns[j-1] + str(i + 2) not in self.moveHistory: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j-1] + str(i + 2) + 'e.p.')
					elif self.board[i][j] == 2: #White Knight:
						knightMoves = []
						##print("White knight moves")
						for l in (-2,-1,1,2):
							for m in (-2,-1,1,2):
								if abs(l) != abs(m) and 0 <= i + l <= 7 and 0 <= j + m <= 7:#Move is not to outside board
									if self.board[i+l][j+m] == 0:#Not taking anything
										knightMoves.append('N' + self.coordinates[i][j] + self.coordinates[i+l][j+m])
									elif self.board[i+l][j+m]  < 0:#Taking pawn
										knightMoves.append('N' + self.coordinates[i][j] + 'x' + self.coordinates[i+l][j+m])
						moves = moves + knightMoves
					elif self.board[i][j] == 3:#White bishop
						bishopMoves = []
						for k in [-1,1]:
							for l in [-1,1]:
								i_count = 1
								j_count = 1
								while 0 <=i + i_count*k <= 7 and 0 <= j + j_count*l <= 7:
									if self.board[i + i_count*k][j + j_count*l] == 0:
										bishopMoves.append('B' + self.coordinates[i][j] + self.coordinates[i + i_count*k][j + j_count*l])
									elif self.board[i + i_count*k][j + j_count*l] < 0:#Taking
										bishopMoves.append('B' + self.coordinates[i][j] + 'x' + self.coordinates[i + i_count*k][j + j_count*l])
										break
									else:
										break
									i_count += 1
									j_count += 1
						moves = moves + bishopMoves
					elif self.board[i][j] == 4:#White rook
						rookMoves = []
						for k in [-1,1]:
							count = 1
							while 0 <= i + count*k <= 7:
								if self.board[i + count*k][j] == 0:
									rookMoves.append('R' + self.coordinates[i][j] + self.coordinates[i + count*k][j])
								elif self.board[i + count*k][j] < 0:
									rookMoves.append('R' + self.coordinates[i][j] + 'x' +self.coordinates[i + count*k][j])
									break
								else:
									break
								count += 1
							count = 1
							while 0 <= j + count*k <= 7:
								if self.board[i][j + count*k] == 0:
									rookMoves.append('R' + self.coordinates[i][j] + self.coordinates[i][j + count*k])
								elif self.board[i][j + count*k] < 0:
									rookMoves.append('R' + self.coordinates[i][j] + 'x' +self.coordinates[i][j + count*k])
									break
								else:
									break
								count += 1
						moves = moves + rookMoves
					elif self.board[i][j] == 5:#White queen
						queenMoves = []
						for k in [-1,1]:
							for l in [-1,1]:
								i_count = 1
								j_count = 1
								while 0 <=i + i_count*k <= 7 and 0 <= j + j_count*l <= 7:
									if self.board[i + i_count*k][j + j_count*l] == 0:
										queenMoves.append('Q' + self.coordinates[i][j] + self.coordinates[i + i_count*k][j + j_count*l])
									elif self.board[i + i_count*k][j + j_count*l] < 0:#Taking
										queenMoves.append('Q' + self.coordinates[i][j] + 'x' + self.coordinates[i + i_count*k][j + j_count*l])
										break
									else:
										break
									i_count += 1
									j_count += 1					
						for k in [-1,1]:
							count = 1
							while 0 <= i + count*k <= 7:
								if self.board[i + count*k][j] == 0:
									queenMoves.append('Q' + self.coordinates[i][j] + self.coordinates[i + count*k][j])
								elif self.board[i + count*k][j] < 0:
									queenMoves.append('Q' + self.coordinates[i][j] + 'x' +self.coordinates[i + count*k][j])
									break
								else:
									break
								count += 1
							count = 1
							while 0 <= j + count*k <= 7:
								if self.board[i][j + count*k] == 0:
									queenMoves.append('Q' + self.coordinates[i][j] + self.coordinates[i][j + count*k])
								elif self.board[i][j + count*k] < 0:
									queenMoves.append('Q' + self.coordinates[i][j] + 'x' +self.coordinates[i][j + count*k])
									break
								else:
									break
								count += 1
						moves = moves + queenMoves
					elif self.board[i][j] == 6:#White king
						kingMoves = []
						for k in [-1,0,1]:
							for l in [-1,0,1]:
								if 0 <= i + k <= 7 and 0 <= j + l <= 7:
									if self.board[i + k][j + l] == 0:
										kingMoves.append('K' + self.coordinates[i][j] + self.coordinates[i + k][j + l])
									elif self.board[i + k][j + l] < 0:
										kingMoves.append('K' + self.coordinates[i][j] + 'x' +self.coordinates[i + k][j + l])
						moves = moves + kingMoves
			if self.canCastleLong(self.sideToMove):
				moves.append("O-O-O")
			if self.canCastleShort(self.sideToMove):
				moves.append("O-O")
			for move in moves:
				self.makeMove(move,False)
				future_checks = self.isCheck()
				if "white" not in future_checks and "black" not in future_checks:
					legal_moves.append(move)
				elif "white" not in future_checks and "black" in future_checks:
					legal_moves.append(move + '+')
				self.undoMove()

		else:#Black to move
			#Pawns
			##print("Black to move")
			for i in range(8):
				for j in range(8):
					if self.board[i][j] == 0:
						continue
					elif self.board[i][j] == -1:#Black pawn
						#One square forward
						if i > 1:
							if self.board[i-1][j] == 0: #and not check
								moves.append(self.pawns[j]+str(i))
						if i == 6:
							#Two squares forward
							if self.board[i-1][j] == 0 and self.board[i-2][j] == 0: #and not check
								moves.append(self.pawns[j]+str(i-1))
						if i == 1 and self.board[i - 1][j] == 0:
							moves.append(self.pawns[j] + "1Q")
							moves.append(self.pawns[j] + "1R")
							moves.append(self.pawns[j] + "1N")
							moves.append(self.pawns[j] + "1B")
						#Taking pawns
						if 0 <= i - 1 <= 5 and 0 <= j + 1 <= 7 and self.board[i - 1][j + 1] > 1:
							if i == 1:
								moves.append(self.pawns[j] + 'x' + self.coordinates[i - 1][j + 1]+ 'Q')
								moves.append(self.pawns[j] + 'x' + self.coordinates[i - 1][j + 1]+ 'R')
								moves.append(self.pawns[j] + 'x' + self.coordinates[i - 1][j + 1]+ 'B')
								moves.append(self.pawns[j] + 'x' + self.coordinates[i - 1][j + 1]+ 'N')
							else:
								moves.append(self.pawns[j] + 'x' + self.coordinates[i - 1][j + 1])
						if 0 <= i - 1 <= 5 and 0 <= j - 1 <= 7 and self.board[i - 1][j - 1] > 1:
							if i == 1:
								moves.append(self.pawns[j] + 'x' + self.coordinates[i - 1][j - 1]+ 'Q')
								moves.append(self.pawns[j] + 'x' + self.coordinates[i - 1][j - 1]+ 'R')
								moves.append(self.pawns[j] + 'x' + self.coordinates[i - 1][j - 1]+ 'B')
								moves.append(self.pawns[j] + 'x' + self.coordinates[i - 1][j - 1]+ 'N')
							else:
								moves.append(self.pawns[j] + 'x' + self.coordinates[i - 1][j - 1])
						if j == 0 and i > 0:
							if self.board[i-1][j+1] == 1: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j+1] + str(i))
							if i == 3 and self.board[i][j+1] == 1 and self.moveHistory[-1] == self.pawns[j+1] + str(i + 1) and self.pawns[j+1] + str(i) not in self.moveHistory: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j+1] + str(i) + 'e.p.')
						if j == 7 and i > 0:
							if self.board[i-1][j-1] == 1: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j-1] + str(i))
							if i == 3 and self.board[i][j-1] == 1 and self.moveHistory[-1] == self.pawns[j-1] + str(i + 1) and self.pawns[j-1] + str(i) not in self.moveHistory: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j-1] + str(i) + 'e.p.')
						elif 0 < j < 7 and i > 0:
							if self.board[i-1][j+1] == 1: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j+1] + str(i))	
							if self.board[i-1][j-1] == 1: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j-1] + str(i))	
							if i == 3 and self.board[i][j+1] == 1 and self.moveHistory[-1] == self.pawns[j+1] + str(i+1) and self.pawns[j+1] + str(i) not in self.moveHistory: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j+1] + str(i) + 'e.p.')
							if i == 3 and self.board[i][j-1] == 1 and self.moveHistory[-1] == self.pawns[j-1] + str(i+1) and self.pawns[j-1] + str(i) not in self.moveHistory: #and not check
								moves.append(self.pawns[j] + 'x' + self.pawns[j-1] + str(i) + 'e.p.')	
					elif self.board[i][j] == -2: #Black Knight:
						knightMoves = []
						###print("Black knight moves")
						for l in (-2,-1,1,2):
							for m in (-2,-1,1,2):
								if abs(l) != abs(m) and 0 <= i + l <= 7 and 0 <= j + m <= 7:#Move is not to outside board
									if self.board[i+l][j+m] == 0:#Not taking anything
										knightMoves.append('N' + self.coordinates[i][j] + self.coordinates[i+l][j+m])
									elif self.board[i+l][j+m]  > 0:#Taking pawn
										knightMoves.append('N' + self.coordinates[i][j] + 'x' + self.coordinates[i+l][j+m])
						moves = moves + knightMoves	
					elif self.board[i][j] == -3:#Black bishop
						bishopMoves = []
						for k in [-1,1]:
							for l in [-1,1]:
								i_count = 1
								j_count = 1
								while 0 <=i + i_count*k <= 7 and 0 <= j + j_count*l <= 7:
									if self.board[i + i_count*k][j + j_count*l] == 0:
										bishopMoves.append('B' + self.coordinates[i][j] + self.coordinates[i + i_count*k][j + j_count*l])
									elif self.board[i + i_count*k][j + j_count*l] > 0:#Taking
										bishopMoves.append('B' + self.coordinates[i][j] + 'x' + self.coordinates[i + i_count*k][j + j_count*l])
										break
									else:
										break
									i_count += 1
									j_count += 1
						moves = moves + bishopMoves
					elif self.board[i][j] == -4:#Black rook
						rookMoves = []
						for k in [-1,1]:
							count = 1
							while 0 <= i + count*k <= 7:
								if self.board[i + count*k][j] == 0:
									rookMoves.append('R' + self.coordinates[i][j] + self.coordinates[i + count*k][j])
								elif self.board[i + count*k][j] > 0:
									rookMoves.append('R' + self.coordinates[i][j] + 'x' +self.coordinates[i + count*k][j])
									break
								else:
									break
								count += 1
							count = 1
							while 0 <= j + count*k <= 7:
								if self.board[i][j + count*k] == 0:
									rookMoves.append('R' + self.coordinates[i][j] + self.coordinates[i][j + count*k])
								elif self.board[i][j + count*k] > 0:
									rookMoves.append('R' + self.coordinates[i][j] + 'x' +self.coordinates[i][j + count*k])
									break
								else:
									break
								count += 1
						moves = moves + rookMoves
					elif self.board[i][j] == -5:#Black queen
						queenMoves = []
						for k in [-1,1]:
							for l in [-1,1]:
								i_count = 1
								j_count = 1
								while 0 <=i + i_count*k <= 7 and 0 <= j + j_count*l <= 7:
									if self.board[i + i_count*k][j + j_count*l] == 0:
										queenMoves.append('Q' + self.coordinates[i][j] + self.coordinates[i + i_count*k][j + j_count*l])
									elif self.board[i + i_count*k][j + j_count*l] > 0:#Taking
										queenMoves.append('Q' + self.coordinates[i][j] + 'x' + self.coordinates[i + i_count*k][j + j_count*l])
										break
									else:
										break
									i_count += 1
									j_count += 1					
						for k in [-1,1]:
							count = 1
							while 0 <= i + count*k <= 7:
								if self.board[i + count*k][j] == 0:
									queenMoves.append('Q' + self.coordinates[i][j] + self.coordinates[i + count*k][j])
								elif self.board[i + count*k][j] > 0:
									queenMoves.append('Q' + self.coordinates[i][j] + 'x' +self.coordinates[i + count*k][j])
									break
								else:
									break
								count += 1
							count = 1
							while 0 <= j + count*k <= 7:
								if self.board[i][j + count*k] == 0:
									queenMoves.append('Q' + self.coordinates[i][j] + self.coordinates[i][j + count*k])
								elif self.board[i][j + count*k] > 0:
									queenMoves.append('Q' + self.coordinates[i][j] + 'x' +self.coordinates[i][j + count*k])
									break
								else:
									break
								count += 1
						moves = moves + queenMoves
					elif self.board[i][j] == -6:#Black king
						kingMoves = []
						for k in [-1,0,1]:
							for l in [-1,0,1]:
								if 0 <= i + k <= 7 and 0 <= j + l <= 7:
									if self.board[i + k][j + l] == 0:
										kingMoves.append('K' + self.coordinates[i][j] + self.coordinates[i + k][j + l])
									elif self.board[i + k][j + l] > 0:
										kingMoves.append('K' + self.coordinates[i][j] + 'x' +self.coordinates[i + k][j + l])
						moves = moves + kingMoves
			if self.canCastleLong(self.sideToMove):
				moves.append("O-O-O")
			if self.canCastleShort(self.sideToMove):
				moves.append("O-O")
			for move in moves:
				self.makeMove(move,False)
				future_checks = self.isCheck()
				if "black" not in future_checks and "white" not in future_checks:
					legal_moves.append(move)
				elif "black" not in future_checks and "white" in future_checks:
					legal_moves.append(move + '+')
				self.undoMove()	
		##print(legal_moves)
		self.moves = legal_moves
		return legal_moves


	def canCastleLong(self, color):
		if color == "white":
			if "white" in self.isCheck():
				return False
			for move in self.moveHistory[::2]:#Long castle
				if move.startswith('K'):
					return False
				elif move.startswith('Ra1'):
					return False
			if self.board[0][1] != 0 or self.board[0][2] != 0 or self.board[0][3] != 0:
				return False 
			for i in range(5):#Pawns and knights
				if self.board[1][i] in [-1, -2, -5, -6]:
					return False
				elif self.board[2][i] == -2:
					return False
			if self.board[1][5] == -2:
				return False
			for start in [(0,1), (0,2), (0,3)]:
				for k in [1]:
					for l in [-1,1]:
						count = 1
						while 0 <= start[0] + count*k <= 7 and 0 <= start[1] + count*l <= 7:
							if self.board[start[0] + count*k][start[1] + count*l] > 0:
								break
							elif self.board[start[0] + count*k][start[1] + count*l] in [-3,-5]:
								return False
							count += 1
					count = 1
					while count <= 7:
						if self.board[count][start[1]] > 0:
							break
						elif self.board[count][start[1]] in [-4,-5]:
							return False
						count += 1
			return True
		else:
			if "black" in self.isCheck():
				return False
			for move in self.moveHistory[1::2]:#Long castle
				if move.startswith('K'):
					return False
				elif move.startswith('Ra8'):
					return False
			if self.board[7][1] != 0 or self.board[7][2] != 0 or self.board[7][3] != 0:
				return False 
			for i in range(5):#Pawns and knights
				if self.board[6][i] in [1, 2, 5, 6]:
					return False
				elif self.board[5][i] == 2:
					return False
			if self.board[6][5] == 2:
				return False
			for start in [(7,1), (7,2), (7,3)]:
				for k in [-1]:
					for l in [-1,1]:
						count = 1
						while 0 <= start[0] + count*k <= 7 and 0 <= start[1] + count*l <= 7:
							if self.board[start[0] + count*k][start[1] + count*l] < 0:
								break
							elif self.board[start[0] + count*k][start[1] + count*l] in [3,5]:
								return False
							count += 1
					count = 6
					while count >= 0:
						if self.board[count][start[1]] < 0:
							break
						elif self.board[count][start[1]] in [4,5]:
							return False
						count -= 1
			return True

	def canCastleShort(self, color):
		if color == "white":
			if "white" in self.isCheck():
				return False
			for move in self.moveHistory[::2]:#Long castle
				if move.startswith('K'):
					return False
				elif move.startswith('Rh1'):
					return False
			if self.board[0][5] != 0 or self.board[0][6] != 0:
				return False 
			for i in range(4,8):#Pawns and knights
				if self.board[1][i] in [-1, -2, -5, -6]:
					return False
				elif self.board[2][i] == -2:
					return False
			if self.board[1][3] == -2:
				return False
			for start in [(0,5), (0,6)]:
				for k in [1]:
					for l in [-1,1]:
						count = 1
						while 0 <= start[0] + count*k <= 7 and 0 <= start[1] + count*l <= 7:
							if self.board[start[0] + count*k][start[1] + count*l] > 0:
								break
							elif self.board[start[0] + count*k][start[1] + count*l] in [-3,-5]:
								return False
							count += 1
					count = 1
					while count <= 7:
						if self.board[count][start[1]] > 0:
							break
						elif self.board[count][start[1]] in [-4,-5]:
							return False
						count += 1
			return True
		else:
			if "black" in self.isCheck():
				return False
			for move in self.moveHistory[1::2]:#Long castle
				if move.startswith('K'):
					return False
				elif move.startswith('Rh8'):
					return False
			if self.board[7][5] != 0 or self.board[7][6]:
				return False 
			for i in range(4,8):#Pawns and knights
				if self.board[6][i] in [1, 2, 5, 6]:
					return False
				elif self.board[5][i] == 2:
					return False
			if self.board[6][3] == 2:
				return False
			for start in [(7,5), (7,6)]:
				for k in [-1]:
					for l in [-1,1]:
						count = 1
						while 0 <= start[0] + count*k <= 7 and 0 <= start[1] + count*l <= 7:
							if self.board[start[0] + count*k][start[1] + count*l] < 0:
								break
							elif self.board[start[0] + count*k][start[1] + count*l] in [3,5]:
								return False
							count += 1
					count = 6
					while count >= 0:
						if self.board[count][start[1]] < 0:
							break
						elif self.board[count][start[1]] in [4,5]:
							return False
						count -= 1
			return True

	def getBoardConfiguration(self, board):
		return np.copy(board)




	def makeMove(self, move,checkMoves=True):
		self.boardHistory.append(self.getBoardConfiguration(self.board))
		color = self.sideToMove
		was_check = False
		if color == 'white':
			color = 1
		else:
			color = -1
		if not self.moves and checkMoves:
			self.moves = self.legalMoves()
		if move not in self.moves and checkMoves:
			##print("Illegal move!")
			return "Illegal move"
		if move.endswith('+'):
			move = move[:-1]
			was_check = True
		#Pawns
		if move[:1] in self.pawns and len(move) == 5:
			if color == 1:
				row = 6
			else:
				row = 1
			self.board[row][self.pawns.index(move[:1])] = 0
			target = move[2:4]
			target = zip(*np.where(self.coordinates == target))[0]
			self.board[row + color][target[1]] = color*self.pieces.index(move[-1])
		elif move[:1] in self.pawns and 'x' not in move and move[-1] not in self.pieces:
			column = self.pawns.index(move[:1])
			###print(color)
			###print(column)
			row = int(move[1:]) - 1
			###print(row)
			self.board[row][column] = color
			if self.board[row - color][column] == color:
				self.board[row - color][column] = 0
			else:
				self.board[row - 2 * color][column] = 0
		elif move[:1] in self.pawns and 'x' in move:
			target = move[2:4]
			###print(target)
			target = zip(*np.where(self.coordinates == target))[0]
			row = target[0]
			column = target[1]
			self.board[row][column] = color
			if 'e.p.' in move:
				self.board[row - color][column] = 0
			column = self.pawns.index(move[:1])
			row = target[0] - color
			self.board[row][column] = 0	
		elif move[:1] in self.pawns and move[-1] in self.pieces:
			if color == 1:
				row = 7
			else:
				row = 0
			self.board[row][self.pawns.index(move[:1])] = color*self.pieces.index(move[-1])
			self.board[row - color][self.pawns.index(move[:1])] = 0
		elif move[:1] == 'N':#Knight move
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
		elif move[:1] == 'B':#Bishop move
			target = move[-2:]
			target = zip(*np.where(self.coordinates == target))[0]
			row = target[0]
			column = target[1]
			self.board[row][column] = color*3
			target = move[1:3]
			target = zip(*np.where(self.coordinates == target))[0]
			row = target[0]
			column = target[1]
			self.board[row][column] = 0	
		elif move[:1] == 'R':#Rook move
			target = move[-2:]
			target = zip(*np.where(self.coordinates == target))[0]
			row = target[0]
			column = target[1]
			self.board[row][column] = color*4
			target = move[1:3]
			target = zip(*np.where(self.coordinates == target))[0]
			row = target[0]
			column = target[1]
			self.board[row][column] = 0	
		elif move[:1] == 'Q':#Rook move
			target = move[-2:]
			target = zip(*np.where(self.coordinates == target))[0]
			row = target[0]
			column = target[1]
			self.board[row][column] = color*5
			target = move[1:3]
			target = zip(*np.where(self.coordinates == target))[0]
			row = target[0]
			column = target[1]
			self.board[row][column] = 0	
		elif move[:1] == 'K':#King move
			target = move[-2:]
			target = zip(*np.where(self.coordinates == target))[0]
			row = target[0]
			column = target[1]
			self.board[row][column] = color*6
			target = move[1:3]
			target = zip(*np.where(self.coordinates == target))[0]
			row = target[0]
			column = target[1]
			self.board[row][column] = 0	
		elif move == "O-O-O":#Long castle
			if color == 1:
				self.board[0][2] = 6
				self.board[0][4] = 0
				self.board[0][0] = 0
				self.board[0][3] = 4
			else:
				self.board[7][2] = -6
				self.board[7][4] = 0
				self.board[7][0] = 0
				self.board[7][3] = -4
		elif move == "O-O":
			if color == 1:
				self.board[0][6] = 6
				self.board[0][4] = 0
				self.board[0][7] = 0
				self.board[0][5] = 4
			else:
				self.board[7][6] = -6
				self.board[7][4] = 0
				self.board[7][7] = 0
				self.board[7][5] = -4				

		self.moves = []
		if was_check:
			self.moveHistory.append(move+'+')
		else:
			self.moveHistory.append(move)
		if color == 1:
			self.sideToMove = 'black'
		else:
			self.sideToMove = 'white'

	def undoMove(self):
		if len(self.moveHistory) == 0:
			##print("No moves have been made!")
			return 0
		###print(self.board == self.boardHistory[-1])
		self.board = self.boardHistory[-1]
		self.boardHistory = self.boardHistory[:-1]
		self.moveHistory = self.moveHistory[:-1]
		if self.sideToMove == "white":
			self.sideToMove = "black"
		else:
			self.sideToMove = "white"

	def isCheck(self,showDiagonal=False):
		#Returns "white" if white is in check, "black" if black is in check
		#Otherwise returns Empty list
		#First check if white king is in check
		checks = []
		diagonalCheckGivers = [3,5]#Bishop,queen
		verticalCheckGivers = [4,5]#Rook, queen

		try:
			whiteKing = zip(*np.where(self.board == 6))[0]
		except:
			self.showBoard()
		whiteKing = zip(*np.where(self.board == 6))[0]
		###print whiteKing
		kingColumn = self.board[:,whiteKing[1]]
		kingColumn = kingColumn[kingColumn != 0]
		kingRow = self.board[whiteKing[0]]
		kingRow = kingRow[kingRow != 0]
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
		###print kingColumn
		###print kingRow
		###print kingRightDiagonal
		###print kingLeftDiagonal

		for row in [kingColumn,kingRow]:
			row = np.insert(row,0,0)
			row = np.append(row,0)
			kingIndex = np.where(row == 6)[0][0]
			if showDiagonal:
				print row	
			in_front = row[kingIndex + 1]			
			if -1*in_front in verticalCheckGivers:
				##print("check from front")
				checks.append("white")
			in_back = row[kingIndex - 1]
			if -1*in_back in verticalCheckGivers:
				checks.append("white")
			
		for row in [kingLeftDiagonal,kingRightDiagonal]:
			row = np.insert(row,0,0)
			row = np.append(row,0)
			if showDiagonal:
				print row
			kingIndex = np.where(row == 6)[0][0]
			in_front = row[kingIndex + 1]
			if -1*in_front in diagonalCheckGivers:
				checks.append("white")
			in_back = row[kingIndex - 1]
			if -1*in_back in diagonalCheckGivers:
				checks.append("white")
			if whiteKing[0] < 7:
				if 0 < whiteKing[1] < 7:
					if self.board[whiteKing[0] + 1][whiteKing[1] + 1] == -1 or self.board[whiteKing[0] + 1][whiteKing[1] - 1] == -1:
						checks.append("white")
				elif whiteKing[1] == 0:
					if self.board[whiteKing[0] + 1][whiteKing[1] + 1] == -1:
						checks.append("white")
				else:
					if self.board[whiteKing[0] + 1][whiteKing[1] - 1] == -1:
						checks.append("white")
		
		#Knights
		for l in (-2,-1,1,2):
			for m in (-2,-1,1,2):
				if abs(l) != abs(m) and 0 <= whiteKing[0] + l <= 7 and 0 <= whiteKing[1] + m <= 7:
					if self.board[whiteKing[0] + l][whiteKing[1] + m] == -2:
						checks.append("white")
		#Kings
		for l in (-1,0,1):
			for m in (-1,0,1):
				if 0 <= whiteKing[0] + l <= 7 and 0 <= whiteKing[1] + m <= 7:
					if self.board[whiteKing[0] + l][whiteKing[1] + m] == -6:
						checks.append("white") 
		
		try:
			blackKing = zip(*np.where(self.board == -6))[0]
		except:
			self.showBoard()
		blackKing = zip(*np.where(self.board == -6))[0]
		###print blackKing
		kingColumn = self.board[:,blackKing[1]]
		kingColumn = kingColumn[kingColumn != 0]
		kingRow = self.board[blackKing[0]]
		kingRow = kingRow[kingRow != 0]
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
		###print kingColumn
		###print kingRow
		###print kingRightDiagonal
		###print kingLeftDiagonal
		for row in [kingColumn,kingRow]:
			row = np.insert(row,0,0)
			row = np.append(row,0)
			kingIndex = np.where(row == -6)[0][0]
			if showDiagonal:
				print row
			in_front = row[kingIndex + 1]
			if in_front in verticalCheckGivers:
				checks.append("black")
			in_back = row[kingIndex - 1]
			if in_back in verticalCheckGivers:
				checks.append("black")
			
		for row in [kingLeftDiagonal,kingRightDiagonal]:
			row = np.insert(row,0,0)
			row = np.append(row,0)
			kingIndex = np.where(row == -6)[0][0]
			if showDiagonal:
				print row
			in_front = row[kingIndex + 1]
			if in_front in diagonalCheckGivers:
				checks.append("black")
			in_back = row[kingIndex - 1]
			if in_back in diagonalCheckGivers:
				checks.append("black")
			if blackKing[0] > 0:
				if 0 < blackKing[1] < 7:
					if self.board[blackKing[0] - 1][blackKing[1] + 1] == 1 or self.board[blackKing[0] - 1][blackKing[1] - 1] == 1:
						checks.append("black")
				elif blackKing[1] == 0:
					if self.board[blackKing[0] - 1][blackKing[1] + 1] == 1:
						checks.append("black")
				else:
					if self.board[blackKing[0] - 1][blackKing[1] - 1] == 1:
						checks.append("black")
			
		#Knights
		for l in (-2,-1,1,2):
			for m in (-2,-1,1,2):
				if abs(l) != abs(m) and 0 <= blackKing[0] + l <= 7 and 0 <= blackKing[1] + m <= 7:
					if self.board[blackKing[0] + l][blackKing[1] + m] == 2:
						checks.append("black")
		#Kings
		for l in (-1,0,1):
			for m in (-1,0,1):
				if 0 <= blackKing[0] + l <= 7 and 0 <= blackKing[1] + m <= 7:
					if self.board[blackKing[0] + l][blackKing[1] + m] == 6:
						checks.append("black")
		##print checks
		return checks


	def gameOver(self):
		if not self.legalMoves():
			checks = self.isCheck()
			if "white" in checks:
				return "black"
			elif "black" in checks:
				return "white"
			else:
				return "stalemate"
		if len(self.moveHistory) >= 100:
			nothing_taken = True
			no_pawn_moves = True
			for move in self.moveHistory[-100:]:
				if 'x' in move:
					nothing_taken = False
					break
				if move[:1] in self.pawns:
					no_pawn_moves = False
					break
			if nothing_taken and no_pawn_moves:
				return "draw by 50 move rule"
		if len(self.moveHistory) >= 12:
			last_moves = self.moveHistory[-12:]
			last_moves_set = set(last_moves)
			last_moves = list(last_moves_set)
			if len(last_moves) <= 4:
				return "draw by repetition"
		unique, counts = np.unique(self.board, return_counts=True)
		piece_counts = dict(zip(unique, counts))
		piece_counts_keys = piece_counts.keys()
		if 1 not in piece_counts_keys and -1 not in piece_counts_keys:
			#print "level 1"
			if 5 not in piece_counts_keys and -5 not in piece_counts_keys:
				#print "level 2"
				if 4 not in piece_counts_keys and -4 not in piece_counts_keys:
					#print "level 3"
					if 3 not in piece_counts_keys and -3 not in piece_counts_keys:
						#print "level 4"
						return "Insufficient material"
					elif (piece_counts.get(3,0) < 2 and piece_counts.get(2,0) == 0 or piece_counts.get(3,0) == 0) and (piece_counts.get(-3,0) < 2 and piece_counts.get(-2,0) == 0 or piece_counts.get(-3,0) == 0):
						#print "level 4 else"
						return "Insufficient material"
		return False


"""
x = Board()
x.newBoard()

x.makeMove('b4')
x.makeMove('f5')
x.makeMove('b5')
x.makeMove('f4')
x.makeMove('b6')
x.makeMove('f3')
x.makeMove('bxc7')
x.makeMove('fxg2')
print x.legalMoves()



gameOver = False

while not gameOver:
	wm = x.legalMoves()
	if "O-O" in wm:
		print "Short castle possible by white!"
	if "O-O-O" in wm:
		"Print long castle possible by white!"
	x.makeMove(wm[randint(0,len(wm)-1)])
	gameOver = x.gameOver()
	if gameOver:
		print gameOver
		break
	bm = x.legalMoves()
	if "O-O" in bm:
		print "Short castle possible by black!"
	if "O-O-O" in bm:
		"Print long castle possible by black!"
	x.makeMove(bm[randint(0,len(bm)-1)])
	gameOver = x.gameOver()
	if gameOver:
		print gameOver
		break

if gameOver == "white" or gameOver == "black":
	x.moveHistory[-1] = x.moveHistory[-1].replace('+','#')
print x.gameOver()
print x.moveHistory
print (len(x.moveHistory))
x.showBoard()
unique, counts = np.unique(x.board, return_counts=True)
piece_counts = dict(zip(unique, counts))
piece_counts_keys = piece_counts.keys()
print piece_counts
print piece_counts_keys
"""