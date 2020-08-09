"""
This class stores all the information about the current gamestate. It will also determine 
all the valid moves for the current state + MoveLog
"""
class Gamestate(object):
	"""docstring for Gamestate"""
	def __init__(self):
		self.board = [
		["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
		["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
		["--", "--", "--", "--", "--", "--", "--", "--"],
		["--", "--", "--", "--", "--", "--", "--", "--"],
		["--", "--", "--", "--", "--", "--", "--", "--"],
		["--", "--", "--", "--", "--", "--", "--", "--"],
		["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
		["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
		]
		self.whiteToMove = True #store whos turn it is
		self.moveLog = [] #Store the moves. Also needs to store all the captured and moved pieces.

		self.whitheKingSq = [7, 4] #Store the position of the white King 
		self.blackKingSq = [0, 4] #Store the position of the black King

		self.checkmate = False
		self.stalemate = False

		self.isCastleMove = False

	def make_move(self, move):
		startRow = move[0][0]
		startCol = move[0][1]
		endRow = move[1][0]
		endCol = move[1][1]
		movedPiece = move[2]
		capturedPiece = move[3]
		## Use this to only execute the move
		self.board[startRow][startCol] = "--"
		self.board[endRow][endCol] = movedPiece
		self.moveLog.append(move)
		self.whiteToMove = not self.whiteToMove
		if movedPiece == "wK":
			self.whitheKingSq = list(move[1])
		elif movedPiece == "bK":
			self.blackKingSq = list(move[1])
		if movedPiece[1] == "p" and (move[1][0] == 0 or move[1][0] == 7):
			self.pawnPromotionPossible = True
			movedPiece = movedPiece[0] + "Q"
			self.board[endRow][endCol] = movedPiece

	def undo_move(self):
		if len(self.moveLog) != 0:
			lastMove = self.moveLog.pop()
			startRow = lastMove[0][0]
			startCol = lastMove[0][1]
			endRow = lastMove[1][0]
			endCol = lastMove[1][1]
			movedPiece = lastMove[2]
			capturedPiece = lastMove[3]
			self.board[endRow][endCol] = capturedPiece
			self.board[startRow][startCol] = movedPiece
			self.whiteToMove = not self.whiteToMove
			if movedPiece == "wK":
				self.whitheKingSq = [startRow, startCol]
			elif movedPiece == "bK":
				self.blackKingSq = [startRow, startCol]

	def generate_all_possible_moves(self):
		moves = []
		for r in range(len(self.board)):
			for c in range(len(self.board)):
				turn = self.board[r][c][0]
				if (self.whiteToMove and turn == "w") or (not self.whiteToMove and turn == "b"):
					piece = self.board[r][c][1]
					'''
					We check for all the pieces and generate its move according to its position
					'''
					if piece == "p":
						self.generate_pawn_moves(r, c, moves)
					elif piece == "R":
						self.generate_rook_moves(r, c, moves)
					elif piece == "N":
						self.generate_knight_moves(r, c, moves)
					elif piece == "B":
						self.generate_bishop_moves(r, c, moves)
					elif piece == "Q":
						self.generate_queen_moves(r, c, moves)
					elif piece == "K":
						self.generate_king_moves(r, c, moves)
		return moves

	def generate_valid_moves(self):
		moves = self.generate_all_possible_moves()
		for i in range(len(moves)-1, -1, -1):
			self.make_move(moves[i])
			self.whiteToMove = not self.whiteToMove
			if self.in_check():
				moves.remove(moves[i])
			self.whiteToMove = not self.whiteToMove
			self.undo_move()

		if len(moves) == 0:
			if self.in_check():
				self.checkmate = True
				print("CHECKMATE")
			else: 
				self.stalemate = True
				print("STALEMATE")
		else:
			self.checkmate = False
			self.stalemate = False

		return moves

	def in_check(self):
		if self.whiteToMove:
			return self.square_under_attack(self.whitheKingSq[0], self.whitheKingSq[1])
		elif not self.whiteToMove:
			return self.square_under_attack(self.blackKingSq[0], self.blackKingSq[1])

	def square_under_attack(self, r, c):
		self.whiteToMove = not self.whiteToMove
		oppMoves = self.generate_all_possible_moves()
		self.whiteToMove = not self.whiteToMove
		for move in oppMoves:
			if move[1][0] == r and move[1][1] == c:
				return True
		return False

	def generate_pawn_moves(self, row, column, moves):
		turn = self.board[row][column][0]
		# This can surely be optimized

		'''
		Logic for all the white Pawns
		'''
		# Check if pawn hasn`t moved yet and if the the squares two rows ahead is empty
		if (turn == "w" and row == 6 and self.board[row - 2][column] == "--" and self.board[row - 1][column] == "--"):
			startSq = [row, column]
			endSq = [row - 2, column] 
			movedPiece = self.board[row][column]
			capturedPiece = self.board[row - 2][column]
			move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
			moves.append(move)

		if (turn == "w" and self.board[row - 1][column] == "--"):
			startSq = [row, column]
			endSq = [row - 1, column] 
			movedPiece = self.board[row][column]
			capturedPiece = self.board[row - 1][column]
			move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
			moves.append(move)

		#capture to the right
		if (turn == "w" and (column+1)<=7 and self.board[row - 1][column + 1][0] == "b"):
			startSq = [row, column]
			endSq = [row - 1, column + 1] 
			movedPiece = self.board[row][column]
			capturedPiece = self.board[row - 1][column + 1]
			move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
			moves.append(move)

		#capture to the left
		if (turn == "w" and (column-1)>=0 and self.board[row - 1][column - 1][0] == "b"):
			startSq = [row, column]
			endSq = [row - 1, column - 1] 
			movedPiece = self.board[row][column]
			capturedPiece = self.board[row - 1][column - 1]
			move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
			moves.append(move)
		'''
		Logic for all the black pawns
		'''
		if (turn == "b" and row == 1 and self.board[row + 2][column] == "--" and self.board[row + 1][column] == "--"):
			startSq = [row, column]
			endSq = [row + 2, column] 
			movedPiece = self.board[row][column]
			capturedPiece = self.board[row + 2][column]
			move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
			moves.append(move)

		if (turn == "b" and self.board[row + 1][column] == "--"):
			startSq = [row, column]
			endSq = [row + 1, column] 
			movedPiece = self.board[row][column]
			capturedPiece = self.board[row + 1][column]
			move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
			moves.append(move) 

		#capture to the right(looking at the board)
		if (turn == "b" and (column+1)<=7 and self.board[row + 1][column + 1][0] == "w"):
			startSq = [row, column]
			endSq = [row + 1, column + 1] 
			movedPiece = self.board[row][column]
			capturedPiece = self.board[row + 1][column + 1]
			move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
			moves.append(move)

		#capture to the left
		if (turn == "b" and (column-1)>=0 and self.board[row + 1][column - 1][0] == "w"):
			startSq = [row, column]
			endSq = [row + 1, column - 1] 
			movedPiece = self.board[row][column]
			capturedPiece = self.board[row + 1][column - 1]
			move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
			moves.append(move)

	def generate_rook_moves(self, row, column, moves):
		#move down
		turn = self.board[row][column][0]
		collison = False
		rowCounter = row
		while collison == False:
			if ((rowCounter + 1) <= 7 and self.board[rowCounter + 1][column] == "--"):
				startSq = [row, column]
				endSq = [rowCounter + 1, column] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[rowCounter + 1][column]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				rowCounter += 1
				## black capture downwards
			elif (turn == "b" and (rowCounter + 1) <= 7 and self.board[rowCounter + 1][column][0] == "w"):
				startSq = [row, column]
				endSq = [rowCounter + 1, column] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[rowCounter + 1][column]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				##white capture downwards
			elif (turn == "w" and (rowCounter + 1) <= 7 and self.board[rowCounter + 1][column][0] == "b"):
				startSq = [row, column]
				endSq = [rowCounter + 1, column] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[rowCounter + 1][column]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
			else:
				collison = True

		#move up
		collison = False
		rowCounter = row
		while collison == False:
			if ((rowCounter - 1) >= 0 and self.board[rowCounter - 1][column] == "--"):
				startSq = [row, column]
				endSq = [rowCounter - 1, column] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[rowCounter - 1][column]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				rowCounter -= 1
				##black captures upwards
			elif (turn == "b" and (rowCounter - 1) >= 0 and self.board[rowCounter - 1][column][0] == "w"):
				startSq = [row, column]
				endSq = [rowCounter - 1, column] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[rowCounter - 1][column]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
			elif (turn == "w" and (rowCounter - 1) >= 0 and self.board[rowCounter - 1][column][0] == "b"):
				startSq = [row, column]
				endSq = [rowCounter - 1, column] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[rowCounter - 1][column]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
			else:
				collison = True

		#move right
		collison = False
		colCounter = column
		while collison == False:
			if ((colCounter + 1) <= 7 and self.board[row][colCounter + 1] == "--"):
				startSq = [row, column]
				endSq = [row, colCounter + 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[row][colCounter + 1]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				colCounter += 1
				## black capture to the right
			elif (turn == "b" and (colCounter + 1) <= 7 and self.board[row][colCounter + 1][0] == "w"):
				startSq = [row, column]
				endSq = [row, colCounter + 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[row][colCounter + 1]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				## white capture to the right
			elif (turn == "w" and (colCounter + 1) <= 7 and self.board[row][colCounter + 1][0] == "b"):
				startSq = [row, column]
				endSq = [row, colCounter + 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[row][colCounter + 1]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
			else:
				collison = True

		#move left
		collison = False
		colCounter = column
		while collison == False:
			if ((colCounter - 1) >= 0 and self.board[row][colCounter - 1] == "--"):
				startSq = [row, column]
				endSq = [row, colCounter - 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[row][colCounter - 1]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				colCounter -= 1
				## black capture to the left
			elif (turn == "b" and (colCounter - 1) >= 0 and self.board[row][colCounter - 1][0] == "w"):
				startSq = [row, column]
				endSq = [row, colCounter - 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[row][colCounter - 1]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				## white capturing to the left
			elif (turn == "w" and (colCounter - 1) >= 0 and self.board[row][colCounter - 1][0] == "b"):
				startSq = [row, column]
				endSq = [row, colCounter - 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[row][colCounter - 1]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
			else:
				collison = True

	def generate_knight_moves(self, row, column, moves):
		'''
		We have a maximum of eight squares we can end up in using the knight
		'''
		turn = self.board[row][column][0]
		SqOne = [row - 2, column - 1]
		SqTwo = [row - 2, column + 1]
		SqThree = [row - 1, column - 2]
		SqFour= [row - 1, column + 2]
		SqFive = [row + 2, column - 1]
		SqSix = [row + 2, column + 1]
		SqSeven = [row + 1, column - 2]
		SqEight = [row + 1, column + 2]
		Squares = [SqOne, SqTwo, SqThree, SqFour, SqFive, SqSix, SqSeven, SqEight]
		for Sq in Squares.copy():
			if (Sq[0]<0 or Sq[0]>7):
				Squares.remove(Sq)
			elif (Sq[1]<0 or Sq[1]>7):
				Squares.remove(Sq)
		for Sq in Squares:
			if (turn == "w" and (self.board[Sq[0]][Sq[1]][0] == "b" or self.board[Sq[0]][Sq[1]] == "--")):
				startSq = [row, column]
				endSq = Sq
				movedPiece = self.board[row][column]
				capturedPiece = self.board[Sq[0]][Sq[1]]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
			if (turn == "b" and (self.board[Sq[0]][Sq[1]][0] == "w" or self.board[Sq[0]][Sq[1]] == "--")):
				startSq = [row, column]
				endSq = Sq
				movedPiece = self.board[row][column]
				capturedPiece = self.board[Sq[0]][Sq[1]]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)

	def generate_bishop_moves(self, row, column, moves):
		turn = self.board[row][column][0]

		collison = False
		counterRow = row
		counterCol = column
		##right and down
		while collison == False:
			inBounds = (counterRow + 1)<=7 and (counterCol + 1)<=7
			if (inBounds and self.board[counterRow + 1][counterCol + 1] == "--"):
				startSq = [row, column]
				endSq = [counterRow + 1 , counterCol + 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow + 1][counterCol + 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				counterCol += 1
				counterRow += 1
				## capture with black
			elif (inBounds and turn == "b" and self.board[counterRow + 1][counterCol + 1][0] == "w"):
				startSq = [row, column]
				endSq = [counterRow + 1 , counterCol + 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow + 1][counterCol + 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				## capture with white
			elif (inBounds and turn == "w" and self.board[counterRow + 1][counterCol + 1][0] == "b"):
				startSq = [row, column]
				endSq = [counterRow + 1 , counterCol + 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow + 1][counterCol + 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
			else:
				collison = True
				

		collison = False
		counterRow = row
		counterCol = column
		##right and up
		while collison == False:
			inBounds = (counterRow - 1)>= 0 and (counterCol + 1)<=7
			if (inBounds and self.board[counterRow - 1][counterCol + 1] == "--"):
				startSq = [row, column]
				endSq = [counterRow - 1 , counterCol + 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow - 1][counterCol + 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				counterCol += 1
				counterRow -= 1
				## capture with black
			elif (inBounds and turn == "b" and self.board[counterRow - 1][counterCol + 1][0] == "w"):
				startSq = [row, column]
				endSq = [counterRow - 1 , counterCol + 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow - 1][counterCol + 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				## capture with white
			elif (inBounds and turn == "w" and self.board[counterRow - 1][counterCol + 1][0] == "b"):
				startSq = [row, column]
				endSq = [counterRow - 1 , counterCol + 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow - 1][counterCol + 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
			else:
				collison = True

		collison = False
		counterRow = row
		counterCol = column
		##left and down
		while collison == False:
			inBounds = (counterRow + 1)<=7 and (counterCol - 1)>=0
			if (inBounds and self.board[counterRow + 1][counterCol - 1] == "--"):
				startSq = [row, column]
				endSq = [counterRow + 1 , counterCol - 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow + 1][counterCol - 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				counterCol -= 1
				counterRow += 1
				## capture with black
			elif (inBounds and turn == "b" and self.board[counterRow + 1][counterCol - 1][0] == "w"):
				startSq = [row, column]
				endSq = [counterRow + 1 , counterCol - 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow + 1][counterCol - 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				## capture with white
			elif (inBounds and turn == "w" and self.board[counterRow + 1][counterCol - 1][0] == "b"):
				startSq = [row, column]
				endSq = [counterRow + 1 , counterCol - 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow + 1][counterCol - 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
			else:
				collison = True
				
		collison = False
		counterRow = row
		counterCol = column
		##left and up
		while collison == False:
			inBounds = (counterRow - 1)>= 0 and (counterCol - 1)>=0
			if (inBounds and self.board[counterRow - 1][counterCol - 1] == "--"):
				startSq = [row, column]
				endSq = [counterRow - 1 , counterCol - 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow - 1][counterCol - 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				counterCol -= 1
				counterRow -= 1
				## capture with black
			elif (inBounds and turn == "b" and self.board[counterRow - 1][counterCol - 1][0] == "w"):
				startSq = [row, column]
				endSq = [counterRow - 1 , counterCol - 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow - 1][counterCol - 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				## capture with white
			elif (inBounds and turn == "w" and self.board[counterRow - 1][counterCol - 1][0] == "b"):
				startSq = [row, column]
				endSq = [counterRow - 1 , counterCol - 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow - 1][counterCol - 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
			else:
				collison = True

	def generate_queen_moves(self, row, column, moves):
		self.generate_bishop_moves(row, column, moves)
		self.generate_rook_moves(row, column, moves)

	def generate_king_moves(self, row, column, moves):
		turn = self.board[row][column][0]

		collison = False
		counterRow = row
		counterCol = column
		##right and down
		while collison == False:
			inBounds = (counterRow + 1)<=7 and (counterCol + 1)<=7
			if (inBounds and self.board[counterRow + 1][counterCol + 1] == "--"):
				startSq = [row, column]
				endSq = [counterRow + 1 , counterCol + 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow + 1][counterCol + 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				## capture with black
			elif (inBounds and turn == "b" and self.board[counterRow + 1][counterCol + 1][0] == "w"):
				startSq = [row, column]
				endSq = [counterRow + 1 , counterCol + 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow + 1][counterCol + 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				## capture with white
			elif (inBounds and turn == "w" and self.board[counterRow + 1][counterCol + 1][0] == "b"):
				startSq = [row, column]
				endSq = [counterRow + 1 , counterCol + 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow + 1][counterCol + 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
			else:
				collison = True
				

		collison = False
		counterRow = row
		counterCol = column
		##right and up
		while collison == False:
			inBounds = (counterRow - 1)>= 0 and (counterCol + 1)<=7
			if (inBounds and self.board[counterRow - 1][counterCol + 1] == "--"):
				startSq = [row, column]
				endSq = [counterRow - 1 , counterCol + 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow - 1][counterCol + 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				## capture with black
			elif (inBounds and turn == "b" and self.board[counterRow - 1][counterCol + 1][0] == "w"):
				startSq = [row, column]
				endSq = [counterRow - 1 , counterCol + 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow - 1][counterCol + 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				## capture with white
			elif (inBounds and turn == "w" and self.board[counterRow - 1][counterCol + 1][0] == "b"):
				startSq = [row, column]
				endSq = [counterRow - 1 , counterCol + 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow - 1][counterCol + 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
			else:
				collison = True

		collison = False
		counterRow = row
		counterCol = column
		##left and down
		while collison == False:
			inBounds = (counterRow + 1)<=7 and (counterCol - 1)>=0
			if (inBounds and self.board[counterRow + 1][counterCol - 1] == "--"):
				startSq = [row, column]
				endSq = [counterRow + 1 , counterCol - 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow + 1][counterCol - 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				## capture with black
			elif (inBounds and turn == "b" and self.board[counterRow + 1][counterCol - 1][0] == "w"):
				startSq = [row, column]
				endSq = [counterRow + 1 , counterCol - 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow + 1][counterCol - 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				## capture with white
			elif (inBounds and turn == "w" and self.board[counterRow + 1][counterCol - 1][0] == "b"):
				startSq = [row, column]
				endSq = [counterRow + 1 , counterCol - 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow + 1][counterCol - 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
			else:
				collison = True
				
		collison = False
		counterRow = row
		counterCol = column
		##left and up
		while collison == False:
			inBounds = (counterRow - 1)>= 0 and (counterCol - 1)>=0
			if (inBounds and self.board[counterRow - 1][counterCol - 1] == "--"):
				startSq = [row, column]
				endSq = [counterRow - 1 , counterCol - 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow - 1][counterCol - 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				## capture with black
			elif (inBounds and turn == "b" and self.board[counterRow - 1][counterCol - 1][0] == "w"):
				startSq = [row, column]
				endSq = [counterRow - 1 , counterCol - 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow - 1][counterCol - 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				## capture with white
			elif (inBounds and turn == "w" and self.board[counterRow - 1][counterCol - 1][0] == "b"):
				startSq = [row, column]
				endSq = [counterRow - 1 , counterCol - 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[counterRow - 1][counterCol - 1] 
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
			else:
				collison = True

		collison = False	
		rowCounter = row
		while collison == False:
			if ((rowCounter + 1) <= 7 and self.board[rowCounter + 1][column] == "--"):
				startSq = [row, column]
				endSq = [rowCounter + 1, column] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[rowCounter + 1][column]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				## black capture downwards
			elif (turn == "b" and (rowCounter + 1) <= 7 and self.board[rowCounter + 1][column][0] == "w"):
				startSq = [row, column]
				endSq = [rowCounter + 1, column] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[rowCounter + 1][column]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				##white capture downwards
			elif (turn == "w" and (rowCounter + 1) <= 7 and self.board[rowCounter + 1][column][0] == "b"):
				startSq = [row, column]
				endSq = [rowCounter + 1, column] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[rowCounter + 1][column]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
			else:
				collison = True

		#move up
		collison = False
		rowCounter = row
		while collison == False:
			if ((rowCounter - 1) >= 0 and self.board[rowCounter - 1][column] == "--"):
				startSq = [row, column]
				endSq = [rowCounter - 1, column] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[rowCounter - 1][column]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				##black captures upwards
			elif (turn == "b" and (rowCounter - 1) >= 0 and self.board[rowCounter - 1][column][0] == "w"):
				startSq = [row, column]
				endSq = [rowCounter - 1, column] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[rowCounter - 1][column]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
			elif (turn == "w" and (rowCounter - 1) >= 0 and self.board[rowCounter - 1][column][0] == "b"):
				startSq = [row, column]
				endSq = [rowCounter - 1, column] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[rowCounter - 1][column]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
			else:
				collison = True

		#move right
		collison = False
		colCounter = column
		while collison == False:
			if ((colCounter + 1) <= 7 and self.board[row][colCounter + 1] == "--"):
				startSq = [row, column]
				endSq = [row, colCounter + 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[row][colCounter + 1]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				## black capture to the right
			elif (turn == "b" and (colCounter + 1) <= 7 and self.board[row][colCounter + 1][0] == "w"):
				startSq = [row, column]
				endSq = [row, colCounter + 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[row][colCounter + 1]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				## white capture to the right
			elif (turn == "w" and (colCounter + 1) <= 7 and self.board[row][colCounter + 1][0] == "b"):
				startSq = [row, column]
				endSq = [row, colCounter + 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[row][colCounter + 1]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
			else:
				collison = True

		#move left
		collison = False
		colCounter = column
		while collison == False:
			if ((colCounter - 1) >= 0 and self.board[row][colCounter - 1] == "--"):
				startSq = [row, column]
				endSq = [row, colCounter - 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[row][colCounter - 1]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				## black capture to the left
			elif (turn == "b" and (colCounter - 1) >= 0 and self.board[row][colCounter - 1][0] == "w"):
				startSq = [row, column]
				endSq = [row, colCounter - 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[row][colCounter - 1]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
				## white capturing to the left
			elif (turn == "w" and (colCounter - 1) >= 0 and self.board[row][colCounter - 1][0] == "b"):
				startSq = [row, column]
				endSq = [row, colCounter - 1] 
				movedPiece = self.board[row][column]
				capturedPiece = self.board[row][colCounter - 1]
				move = [startSq, endSq, movedPiece, capturedPiece, self.isCastleMove]
				moves.append(move)
				collison = True
			else:
				collison = True





