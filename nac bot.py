# imports

import pygame
import numpy
import copy

pygame.init()

class game:

    # main functions

    def __init__(self,board,playerPiece):
        self.playerPiece = playerPiece
        self.botPiece = playerPiece * -1
        self.turn = 1
        self.status = 2 # 2: ongoing, 1: X win, 0: draw, -1: O win
        self.board = board


    def update(self,keys):

        # making sure nothing happens if someones won
        self.status = eval(self.board)
        if self.status != 2:
            return self.status

        # player move handling
        elif self.turn == self.playerPiece:
            for square in squareNums:
                if keys[ord(str(square))]:
                    move = convertTo2D(square)
                    if self.validMove(move):
                        self.board[move[0]][move[1]] = self.playerPiece
                        self.turn = self.turn * -1

        # bot move handling
        elif self.turn == self.botPiece:
            self.board = self.getBestMove()
            self.turn = self.turn * -1

        return self.status
            

    # game logic functions

    # assuming the game is not over
    # checks if a move can be played
    def validMove(self,m):
        if self.board[m[0]][m[1]] == 0:
            return True
        else:
            return False
        
    
    def getBestMove(self):
        childBoards = getChildBoards(self.board,self.turn)
        evals = []
        for board in childBoards:
            evals.append(minimax(board,10,-1,1,self.turn*-1))
        
        print(evals)

        if self.botPiece == 1:
            bestEvalIndex = evals.index(max(evals))
        elif self.botPiece == -1:
            bestEvalIndex = evals.index(min(evals))

        bestBoard = childBoards[bestEvalIndex]
        return bestBoard

    
    # gui functions

    def drawBoard(self):

        # board frame

        pygame.draw.rect(screen,"white",((bLeft,bTop),(bWidth,bHeight)),10)
        
        for i in range(3):
            rowY = bTop + (i/3) * bHeight
            columnX = bLeft + (i/3) * bWidth

            pygame.draw.line(screen,"white",(bLeft,rowY),(bRight,rowY),10) # rows
            pygame.draw.line(screen,"white",(columnX,bTop),(columnX,bBottom),10) # columns

        # square contents

        for i in range(3):
            for j in range(3):
                drawPiece(self.board[i][j],(j,i))

    
# functions


# returns the pygame rect value of a square on the board
def getSquareRect(pos):

    sLeft = bLeft + (pos[0]/3) * bWidth
    sTop = bTop + (pos[1]/3) * bHeight

    sWidth = bWidth/3
    sHeight = bHeight/3

    sRect = ((sLeft,sTop),(sWidth,sHeight))
    return sRect


def getSquareCorners(pos):
    sLeft = bLeft + (pos[0]/3) * bWidth
    sRight = sLeft + (1/3) * bWidth

    sTop = bTop + (pos[1]/3) * bHeight
    sBottom = sTop + (1/3) * bWidth

    bl = (sLeft,sBottom)
    br = (sRight,sBottom)
    tl = (sLeft,sTop)
    tr = (sRight,sTop)

    return bl,br,tl,tr


def drawPiece(piece,pos):
        if piece == -1:
            sRect = getSquareRect(pos)
            pygame.draw.ellipse(screen,"red",sRect,10)
        elif piece == 1:
            bl,br,tl,tr = getSquareCorners(pos)
            pygame.draw.line(screen,"blue",bl,tr,10)
            pygame.draw.line(screen,"blue",br,tl,10)


# gets all possible moves the guy can make
def getChildBoards(board,player):
    childBoards = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                child = copy.deepcopy(board)
                child[i][j] = player
                childBoards.append(child)
    return childBoards


def convertTo2D(num):
    num = num - 1
    return (num//3,num%3)
    

# returns the positional evaluation of an ongoing game
def minimax(board,depth,alpha,beta,player):
    boardEval = eval(board)

    if depth == 0 or boardEval != 2:
        return boardEval
        
    if player == 1:
        childBoards = getChildBoards(board,1)
        maxEval = -1
        for child in childBoards:
            maxEval = max(maxEval,minimax(child,depth-1,alpha,beta,-1))
            if maxEval >= beta:
                break
            alpha = max(alpha,maxEval)
        return maxEval

    else:
        minEval = 1
        childBoards = getChildBoards(board,-1)
        for child in childBoards:
            minEval = min(minEval,minimax(child,depth-1,alpha,beta,1))
            if minEval <= alpha:
                break
            beta = min(beta,minEval)
        return minEval


# returns : 2: ongoing, 1: X win, 0: draw, -1: O win
# evaluates the status of a board
def eval(board):
    
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != 0:
            return board[i][0]  # row 
        if board[0][i] == board[1][i] == board[2][i] != 0:
            return board[0][i]  # column 

    # diagonals
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]

    # check for draw
    draw = True
    for i in range(3):
        if 0 in board[i]: # if game not full
            draw = False
            break
    if draw == True:
        return 0 # draw
        
    return 2 # ongoing


# pygame stuff

# screen res can be altered at will
screenRes = (800,800)
clock = pygame.time.Clock()
fps = 60
dt = 1/fps
screen = pygame.display.set_mode(screenRes)

# settings

running = True
bgColour = "grey"
squareNums = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# board dimensions (based from screen resolution)

bFrac = 3/4
bScale = (1 - bFrac) * 0.5

bWidth = screenRes[0] * bFrac
bHeight = screenRes[1] * bFrac

bLeft = screenRes[0]*bScale
bRight = screenRes[0]-bLeft

bTop = screenRes[1]*bScale
bBottom = screenRes[1]-bTop

bTopLeft = (bLeft,bTop)
bTopRight = (bRight,bTop)

bBottomLeft = (bLeft,bBottom)
bBottomRight = (bRight,bBottom)


game1 = game([[0,0,0],[0,0,0],[0,0,0]],1)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False

    if not running:
        break

    screen.fill(bgColour)

    game1.drawBoard()
    game1.update(keys)


    pygame.display.flip()

    dt = clock.tick(fps)
