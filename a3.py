### help from https://medium.com/byte-tales/the-classic-tic-tac-toe-game-in-python-3-1427c68b8874
### to create the board
### https://stackoverflow.com/questions/5105517/deep-copy-of-a-dict-in-python
### getting deep copy of dictionary


import random as r
import copy 

def printBoard(board):
	print(board[1] + '|' + board[2] + '|' + board[3])
	print("-----")
	print(board[4] + '|' + board[5] + '|' + board[6])
	print("-----")
	print(board[7] + '|' + board[8] + '|' + board[9])
	return

def updateBoard(board,mark,pos):
	if(board[pos] == ' '):
		board[pos] = mark
		return board
	else:
		print('This is not a valid move')
		return

def checkVictory(board):
	if((board[1] == board[2] == board[3]) and (board[1] != ' ' and board[2] != ' ' and board[3] != ' ')):
		return True 
	elif((board[4] == board[5] == board[6]) and (board[4] != ' ' and board[5] != ' ' and board[6] != ' ')):
		return True
	elif((board[7] == board[8] == board[9]) and (board[7] != ' ' and board[8] != ' ' and board[9] != ' ')):
		return True
	elif((board[1] == board[4] == board[7]) and (board[1] != ' ' and board[4] != ' ' and board[7] != ' ')):
		return True
	elif((board[2] == board[5] == board[8]) and (board[2] != ' ' and board[5] != ' ' and board[8] != ' ')):
		return True
	elif((board[3] == board[6] == board[9]) and (board[3] != ' ' and board[6] != ' ' and board[9] != ' ')):
		return True
	elif((board[1] == board[5] == board[9]) and (board[1] != ' ' and board[5] != ' ' and board[9] != ' ')):
		return True
	elif((board[3] == board[5] == board[7]) and (board[3] != ' ' and board[5] != ' ' and board[7] != ' ')):
		return True
	else:
		return False 


def checkLegalMoves(board):
	legalMoves = []
	for i in range(1,10):
		if(board[i] == ' '):
			legalMoves.append(i)
	return legalMoves

## win = +1 draw = +1/2 lose = 0
def playout(board,legalMoves,OGmark,movenum,order):
	scoring = {}
	for i in legalMoves:
		scoring[i] = 0
	print(scoring)
	for i in legalMoves:
		print("-"*32)
		print("This legal move: " + str(i))
		print("-"*32)
		simBoard = copy.deepcopy(board)
		### for loop running however many tests
		inMoveNum = movenum
		simBoard = updateBoard(simBoard,OGmark,i)
		inMoveNum += 1
		haveWinner = checkVictory(simBoard)

		if(order == 1):
			haveWinner = False
			while(not haveWinner and inMoveNum != 9):
				printBoard(simBoard)
				if(inMoveNum % 2 == 0):
					#computer turn
					mark = 'O'
					inlegalMoves = checkLegalMoves(simBoard)
					print(inlegalMoves)
					print("Simulated O")
					simBoard = updateBoard(simBoard,mark,r.choice(inlegalMoves))
					inMoveNum += 1
					haveWinner = checkVictory(simBoard)
				else:
					#human turn
					mark = 'X'
					inlegalMoves = checkLegalMoves(simBoard)
					print(inlegalMoves)
					print("Simulated X")
					simBoard = updateBoard(simBoard,mark,r.choice(inlegalMoves))
					inMoveNum += 1
					haveWinner = checkVictory(simBoard)
			printBoard(simBoard)
			print("-"*10+"Result"+"-"*10)
			if(not haveWinner):
				print("Draw " + str(i))
				scoring[i] += 0.5
			elif(inMoveNum % 2 == 0):
				print("Loss " + str(i))
			elif(inMoveNum % 2 == 1):
				print("Win " + str(i))
				scoring[i] += 1
			print("-"*10+"Result"+"-"*10)
		elif(order == 2):
			haveWinner = False
			while(not haveWinner and inMoveNum != 9):
				printBoard(simBoard)
				if(inMoveNum % 2 == 0):
					#computer turn
					mark = 'O'
					inlegalMoves = checkLegalMoves(simBoard)
					print(inlegalMoves)
					print("Simulated O")
					simBoard = updateBoard(simBoard,mark,r.choice(inlegalMoves))
					inMoveNum += 1
					haveWinner = checkVictory(simBoard)
				else:
					#human turn
					mark = 'X'
					inlegalMoves = checkLegalMoves(simBoard)
					print(inlegalMoves)
					print("Simulated X")
					simBoard = updateBoard(simBoard,mark,r.choice(inlegalMoves))
					inMoveNum += 1
					haveWinner = checkVictory(simBoard)
			printBoard(simBoard)
			print("-"*10+"Result"+"-"*10)
			if(not haveWinner):
				print("Draw " + str(i))
				scoring[i] += 0.5
			elif(inMoveNum % 2 == 0):
				print("Win " + str(i))
				scoring[i] += 1
			elif(inMoveNum % 2 == 1):
				print("Loss " + str(i))
			print("-"*10+"Result"+"-"*10)
	print(scoring)
	maximum = max(scoring,key=scoring.get)
	print("MAX: " + str(maximum))

	return

def playOrder():
	return r.choice([1,2])

def game(order):
	newBoard = {1:' ',2:' ',3:' ',4:' ',5:' ',6:' ',7:' ',8:' ',9:' '}
	haveWinner = False
	movenum = 0
	if(order == 1): # order 1 is when computer is O
		while(not haveWinner and movenum != 9):
			printBoard(newBoard)
			if(movenum % 2 == 0):
				#computer turn
				mark = 'O'
				legalMoves = checkLegalMoves(newBoard)
				print(legalMoves)
				print("Computer")

				playout(newBoard,legalMoves,mark,movenum,order)

				newBoard = updateBoard(newBoard,mark,r.choice(legalMoves))
				movenum += 1
				haveWinner = checkVictory(newBoard)
			else:
				#human turn
				mark = 'X'
				move = input("Make your last pathetic move Yugi: ")
				newBoard = updateBoard(newBoard,mark,int(move))
				movenum += 1
				haveWinner = checkVictory(newBoard)
		printBoard(newBoard)
		if(not haveWinner):
			print("No one Wins...")
		elif(movenum % 2 == 0):
			print("Kaiba Wins!")
		elif(movenum % 2 == 1):
			print("Computer Wins!")
	elif(order == 2): # order 2 is when computer is X
		while(not haveWinner and movenum != 9):
			printBoard(newBoard)
			if(movenum % 2 == 0):
				#human turn
				mark = 'O'
				move = input("Make your last pathetic move Yugi: ")
				newBoard = updateBoard(newBoard,mark,int(move))
				movenum += 1
				haveWinner = checkVictory(newBoard)
			else:
				#computer turn
				mark = 'X'
				legalMoves = checkLegalMoves(newBoard)
				print(legalMoves)
				print("Computer")

				playout(newBoard,legalMoves,mark,movenum,order)

				newBoard = updateBoard(newBoard,mark,r.choice(legalMoves))
				movenum += 1
				haveWinner = checkVictory(newBoard)
		printBoard(newBoard)
		if(not haveWinner):
			print("No one Wins...")
		elif(movenum % 2 == 0):
			print("Computer Wins!")
		elif(movenum % 2 == 1):
			print("Kaiba Wins!")
		

order = playOrder()
game(order)



# printBoard(newBoard)
# newBoard = updateBoard(newBoard,mark,3)
# movenum += 1
# printBoard(newBoard)
