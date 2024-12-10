import pygame
import random
import copy

#  utility functions
#This function returns a list of valid neighboring cells around a given (x, y) coordinate,
#  within the bounds of the grid.
#  It checks in all 8 possible directions (left, right, up, down, and diagonals).
def directions(x, y, minX=0, minY=0, maxX=7, maxY=7):
    """Check to determine which directions are valid from current cell"""
    validdirections = []
    if x != minX: validdirections.append((x-1, y))
    if x != minX and y != minY: validdirections.append((x-1, y-1))
    if x != minX and y != maxY: validdirections.append((x-1, y+1))

    if x!= maxX: validdirections.append((x+1, y))
    if x != maxX and y != minY: validdirections.append((x+1, y-1))
    if x != maxX and y != maxY: validdirections.append((x+1, y+1))

    if y != minY: validdirections.append((x, y-1))
    if y != maxY: validdirections.append((x, y+1))

    return validdirections

#Loads an image from the specified file path, scales it to the provided size,
#  and returns the image object for use in the game.
def loadImages(path, size):
    """Load an image into the game, and scale the image"""
    img = pygame.image.load(f"{path}").convert_alpha()
    img = pygame.transform.scale(img, size)
    return img


#Loads a section of a sprite sheet (image with multiple frames), 
# scales it to the desired size, and returns it for use (e.g., in animations).
def loadSpriteSheet(sheet, row, col, newSize, size):
    """creates an empty surface, loads a portion of the spritesheet onto the surface, then return that surface as img"""
    image = pygame.Surface((32, 32)).convert_alpha()
    image.blit(sheet, (0, 0), (row * size[0], col * size[1], size[0], size[1]))
    image = pygame.transform.scale(image, newSize)
    image.set_colorkey('Black')
    return image

#Evaluates the board by calculating a score for the current game state. 
# It currently just calculates the total number of opponent tiles
#  on the board (though this is a simplified scoring mechanism).
def evaluateBoard(grid, player):
    score = 0
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            score -= col
    return score

#  Classes
#Othello is the main game class. It initializes the game, handles user input,
#  updates game logic, and renders the game on the screen.
# Main attributes:
# player1 and player2: Represent player pieces (1 = white, -1 = black).
# currentPlayer: Keeps track of which player’s turn it is.
# grid: An instance of the Grid class that manages the game board.
# computerPlayer: Instance of ComputerPlayer, which is the AI opponent.
class Othello:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1100, 800))
        pygame.display.set_caption('Othello')

        self.player1 = 1
        self.player2 = -1

        self.currentPlayer = 1

        self.time = 0

        self.rows = 8
        self.columns = 8

        self.gameOver = True

        self.grid = Grid(self.rows, self.columns, (80, 80), self)
        self.computerPlayer = ComputerPlayer(self.grid)

        self.RUN = True


#The main game loop, which handles input, updates, and rendering.
    def run(self):
        while self.RUN == True:
            self.input()
            self.update()
            self.draw()


#Manages user inputs, such as mouse clicks for placing tokens or restarting the game.
    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUN = False

            if event.type == pygame.MOUSEBUTTONDOWN: #this means right click of mouse(it will show current logic of game)
                if event.button == 3:
                    self.grid.printGameLogicBoard()

                if event.button == 1: #checks for left click
                    if self.currentPlayer == 1 and not self.gameOver:
                        x, y = pygame.mouse.get_pos()  #position of cursor in coordinates
                        x, y = (x - 80) // 80, (y - 80) // 80 #adjusting for 80 pixel border and each cell of size 80
                        validCells = self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer) 
                        if not validCells:
                            pass
                        else:
                            if (y, x) in validCells:
                                self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, y, x)
                                swappableTiles = self.grid.swappableTiles(y, x, self.grid.gridLogic, self.currentPlayer)
                                for tile in swappableTiles:
                                    self.grid.animateTransitions(tile, self.currentPlayer)
                                    self.grid.gridLogic[tile[0]][tile[1]] *= -1
                                self.currentPlayer *= -1
                                self.time = pygame.time.get_ticks()

                    if self.gameOver:
                        x, y = pygame.mouse.get_pos()
                        if x >= 320 and x <= 480 and y >= 400 and y <= 480:
                            self.grid.newGame()
                            self.gameOver = False

#Handles game logic updates, including managing turns and checking for valid moves.
    def update(self):
        if self.currentPlayer == -1:
            new_time = pygame.time.get_ticks() #no. of milliseconds since the game started
            if new_time - self.time >= 100: #to introduce a slight delay before computer makes its move
                if not self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer):
                    self.gameOver = True
                    return
                cell, score = self.computerPlayer.computerHard(self.grid.gridLogic, 5, -64, 64, -1)
                #evaluates the board state to a depth of 5 moves, with -64 as the worst possible score
                #  and 64 as the best possible score. that is the actual minimax, alpha beta pruning

                self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, cell[0], cell[1])
                swappableTiles = self.grid.swappableTiles(cell[0], cell[1], self.grid.gridLogic, self.currentPlayer)
                #This returns a list of tokens that need to be flipped after the computer move.
                for tile in swappableTiles:
                    self.grid.animateTransitions(tile, self.currentPlayer)
                    self.grid.gridLogic[tile[0]][tile[1]] *= -1
                self.currentPlayer *= -1

        self.grid.player1Score = self.grid.calculatePlayerScore(self.player1)
        self.grid.player2Score = self.grid.calculatePlayerScore(self.player2)
        if not self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer):
            self.gameOver = True
            return

#Renders the game board, scores, and pieces.
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.grid.drawGrid(self.screen)
        pygame.display.update()


#The Grid class represents the Othello game board.

# It manages the grid logic (gridLogic) and the graphical display (gridBg).
# gridLogic is an 8x8 matrix where each cell stores the state (empty = 0, player1 = 1, player2 = -1).
# tokens is a dictionary to store each token on the board for drawing purposes.
class Grid:
    def __init__(self, rows, columns, size, main):
        self.GAME = main
        self.y = rows
        self.x = columns
        self.size = size
        self.whitetoken = loadImages('assets/WhiteToken.png', size)
        self.blacktoken = loadImages('assets/BlackToken.png', size)
        self.transitionWhiteToBlack = [loadImages(f'assets/BlackToWhite{i}.png', self.size) for i in range(1, 4)]
        self.transitionBlackToWhite = [loadImages(f'assets/WhiteToBlack{i}.png', self.size) for i in range(1, 4)]
        self.bg = self.loadBackGroundImages()

        self.tokens = {}

        self.gridBg = self.createbgimg()

        self.gridLogic = self.regenGrid(self.y, self.x)

        self.player1Score = 0
        self.player2Score = 0

        self.font = pygame.font.SysFont('Arial', 20, True, False)

#Resets the game board.
    def newGame(self):
        self.tokens.clear()
        self.gridLogic = self.regenGrid(self.y, self.x)

#Load and generate the background of the game grid.
    def loadBackGroundImages(self):
        alpha = 'ABCDEFGHI'
        spriteSheet = pygame.image.load('assets/wood.png').convert_alpha()
        imageDict = {}
        for i in range(3):
            for j in range(7):
                imageDict[alpha[j]+str(i)] = loadSpriteSheet(spriteSheet, j, i, (self.size), (32, 32))
        return imageDict

    def createbgimg(self):
        gridBg = [
            ['C0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'E0'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'E2'],
        ]
        image = pygame.Surface((960, 960))
        for j, row in enumerate(gridBg):
            for i, img in enumerate(row):
                image.blit(self.bg[img], (i * self.size[0], j * self.size[1]))
        return image

    def regenGrid(self, rows, columns):
        """generate an empty grid for logic use"""
        grid = []
        for y in range(rows):
            line = []
            for x in range(columns):
                line.append(0)
            grid.append(line)
        self.insertToken(grid, 1, 3, 3)
        self.insertToken(grid, -1, 3, 4)
        self.insertToken(grid, 1, 4, 4)
        self.insertToken(grid, -1, 4, 3)

        return grid

    def calculatePlayerScore(self, player):
        score = 0
        for row in self.gridLogic:
            for col in row:
                if col == player:
                    score += 1
        return score

    def drawScore(self, player, score):
        textImg = self.font.render(f'{player} : {score}', 1, 'White')
        return textImg

    def endScreen(self):
        if self.GAME.gameOver:
            endScreenImg = pygame.Surface((320, 320))
            endText = self.font.render(f'{"Congratulations, You Won!!" if self.player1Score > self.player2Score else "Bad Luck, You Lost"}', 1, 'White')
            endScreenImg.blit(endText, (0, 0))
            newGame = pygame.draw.rect(endScreenImg, 'White', (80, 160, 160, 80))
            newGameText = self.font.render('Play Again', 1, 'Black')
            endScreenImg.blit(newGameText, (120, 190))
        return endScreenImg

#Draws the game board, tokens, available moves, and the end screen if the game is over.
    def drawGrid(self, window):
        window.blit(self.gridBg, (0, 0))

        window.blit(self.drawScore('White', self.player1Score), (900, 100))
        window.blit(self.drawScore('Black', self.player2Score), (900, 200))

        for token in self.tokens.values():
            token.draw(window)

        availMoves = self.findAvailMoves(self.gridLogic, self.GAME.currentPlayer)
        if self.GAME.currentPlayer == 1:
            for move in availMoves:
                pygame.draw.rect(window, 'White', (80 + (move[1] * 80) + 30, 80 + (move[0] * 80) + 30, 20, 20))

        if self.GAME.gameOver:
            window.blit(self.endScreen(), (240, 240))

    def printGameLogicBoard(self):
        print('  | A | B | C | D | E | F | G | H |')
        for i, row in enumerate(self.gridLogic):
            line = f'{i} |'.ljust(3, " ")
            for item in row:
                line += f"{item}".center(3, " ") + '|'
            print(line)
        print()

    def findValidCells(self, grid, curPlayer):
        """Performs a check to find all empty cells that are adjacent to opposing player"""
        validCellToClick = []
        for gridX, row in enumerate(grid):
            for gridY, col in enumerate(row):
                if grid[gridX][gridY] != 0: #dont consider non empty cells
                    continue
                DIRECTIONS = directions(gridX, gridY)

                for direction in DIRECTIONS:
                    dirX, dirY = direction
                    checkedCell = grid[dirX][dirY]

                    if checkedCell == 0 or checkedCell == curPlayer: #if currplayer,then leave
                        continue

                    if (gridX, gridY) in validCellToClick: #if already considered then leave
                        continue

                    validCellToClick.append((gridX, gridY)) #if none of the above, then add to list
        return validCellToClick

#Checks for and returns the tiles that can be flipped if a move is made at (x, y).
    def swappableTiles(self, x, y, grid, player):
        surroundCells = directions(x, y) #get valid surrounding cells
        if len(surroundCells) == 0:
            return []

        swappableTiles = []
        for checkCell in surroundCells:
            checkX, checkY = checkCell
            difX, difY = checkX - x, checkY - y #difference between cell to check and current cell
            currentLine = []

            RUN = True
            while RUN:
                if grid[checkX][checkY] == player * -1:
                    currentLine.append((checkX, checkY)) #if opponent token, add to list
                elif grid[checkX][checkY] == player: #if own token, break
                    RUN = False
                    break
                elif grid[checkX][checkY] == 0: #if empty space, empty list and ignore
                    currentLine.clear()
                    RUN = False
                checkX += difX
                checkY += difY

                if checkX < 0 or checkX > 7 or checkY < 0 or checkY > 7:    #if checkX and checkY 
                                                                            #out of bounds, empty the list
                    currentLine.clear()
                    RUN = False

            if len(currentLine) > 0:
                swappableTiles.extend(currentLine) #add current list to final ans

        return swappableTiles

#Finds all available valid moves for the current player.
    def findAvailMoves(self, grid, currentPlayer):
        """Takes the list of validCells and checks each to see if playable"""
        validCells = self.findValidCells(grid, currentPlayer)
        playableCells = []

        for cell in validCells:
            x, y = cell
            if cell in playableCells:
                continue
            swapTiles = self.swappableTiles(x, y, grid, currentPlayer)

            #if len(swapTiles) > 0 and cell not in playableCells:
            #If the swapTiles list is not empty (meaning that placing a token at (x, y)
            #  would result in flipping at least one of the opponent's tokens)
            # , this cell is considered a valid move.
            if len(swapTiles) > 0:
                playableCells.append(cell)
        #returns the list playableCells, which contains all the coordinates where
        #  the current player can legally place a token to flip opponent tokens.
        return playableCells

#Inserts a token for the current player on the board at (x, y) and updates the board state.
    def insertToken(self, grid, curplayer, y, x):
        tokenImage = self.whitetoken if curplayer == 1 else self.blacktoken
        self.tokens[(y, x)] = Token(curplayer, y, x, tokenImage, self.GAME)
        grid[y][x] = self.tokens[(y, x)].player

#Handles animations for flipping tiles.
    def animateTransitions(self, cell, player):
        if player == 1:
            self.tokens[(cell[0], cell[1])].transition(self.transitionWhiteToBlack, self.whitetoken)
        else:
            self.tokens[(cell[0], cell[1])].transition(self.transitionBlackToWhite, self.blacktoken)

#Represents a single token on the board. It has methods for transitioning its image
#  when flipped and drawing itself on the screen.
class Token:
    def __init__(self, player, gridX, gridY, image, main):
        self.player = player
        self.gridX = gridX
        self.gridY = gridY
        self.posX = 80 + (gridY * 80)
        self.posY = 80 + (gridX * 80)
        self.GAME = main

        self.image = image

    def transition(self, transitionImages, tokenImage):
        for i in range(30):
            self.image = transitionImages[i // 10]
            self.GAME.draw()
        self.image = tokenImage

    def draw(self, window):
        window.blit(self.image, (self.posX, self.posY))

#This class implements the AI opponent.
#  It uses a recursive minimax algorithm with alpha-beta pruning to determine the best move.
class ComputerPlayer:
    def __init__(self, gridObject):
        self.grid = gridObject


# The minimax algorithm that looks ahead depth moves to find the optimal move for the AI.
# grid: The current game board (a 2D array).
# depth: The depth of the recursion or the number of moves the AI looks ahead to make a decision.
# alpha: Represents the best score that the maximizer (computer) can guarantee at the current level or above.
# beta: Represents the best score that the minimizer (human or opponent) can guarantee at the current level or above.
# player: The current player making the move (1 for the human, -1 for the computer).
    def computerHard(self, grid, depth, alpha, beta, player):
        #A new copy of the board is created (newGrid) so that the original board
        #  remains unmodified during recursive evaluations.
        newGrid = copy.deepcopy(grid)
        availMoves = self.grid.findAvailMoves(newGrid, player)

        #If the recursion depth reaches 0 (i.e., it stops looking further ahead)
        # or there are no available moves for the current player, 
        # the function returns the current board evaluation using the evaluateBoard() function.
        if depth == 0 or len(availMoves) == 0:
            bestMove, Score = None, evaluateBoard(grid, player)
            return bestMove, Score

        # Maximizing player (player == -1): This is the computer, which tries to maximize its score.
        # Minimizing player (player == 1): This is the human (or opponent),
        #  which tries to minimize the computer’s score.


        #Initially, the bestScore is set to a very low value (-64),
        #  meaning the AI wants to improve on this.
        #The availMoves list contains all possible moves the computer can make.
        #  The function goes through each move to simulate its impact on the game.
        if player < 0:
            bestScore = -64
            bestMove = None

            for move in availMoves:
                x, y = move 
                # do the move and check the swappable tiles
                swappableTiles = self.grid.swappableTiles(x, y, newGrid, player) 
                newGrid[x][y] = player #mark the coordinate as current player
                for tile in swappableTiles:
                    newGrid[tile[0]][tile[1]] = player #mark all swappable tile as current player


                #recursively call the funcion for the opponent player to evaluate his moves
                bMove, value = self.computerHard(newGrid, depth-1, alpha, beta, player *-1)
                #If the new board's score is better than bestScore, it updates bestMove and bestScore.
                if value > bestScore:
                    bestScore = value
                    bestMove = move

                #It also updates alpha, the best score the maximizer (computer) can guarantee:
                alpha = max(alpha, bestScore)
                # If beta <= alpha, the function prunes further exploration since
                # it knows that no further moves can provide a better outcome. 
                if beta <= alpha:
                    break

                newGrid = copy.deepcopy(grid)
            return bestMove, bestScore


        #below part is for the opponent:
        #Similar to the maximizer, but now the goal is to minimize the score. 
        # bestScore is initialized to a very high value (64), 
        # meaning the opponent is trying to lower it.
        if player > 0:
            bestScore = 64
            bestMove = None

            for move in availMoves:
                x, y = move
                swappableTiles = self.grid.swappableTiles(x, y, newGrid, player)
                newGrid[x][y] = player
                for tile in swappableTiles:
                    newGrid[tile[0]][tile[1]] = player

                bMove, value = self.computerHard(newGrid, depth-1, alpha, beta, player)
                #Place the token and flip opponent’s tokens.
                # Recursively call computerHard().
                # Compare the result with bestScore and update beta,
                #  which represents the best score the minimizer can guarantee.
                if value < bestScore:
                    bestScore = value
                    bestMove = move
                beta = min(beta, bestScore)
                if beta <= alpha:
                    break
                #If beta <= alpha, further exploration is stopped
                #  as the result won’t improve for the opponent.

                newGrid = copy.deepcopy(grid)
            return bestMove, bestScore
            #Depth: It looks ahead multiple moves (depending on depth) to anticipate
            #  the outcome of each move.
            # Alpha-Beta Pruning: It optimizes the process by cutting off branches of the game
            #  tree that don’t need to be explored, improving efficiency.
            
if __name__ == '__main__':
    game = Othello()
    game.run()
    pygame.quit()