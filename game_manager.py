import constants

class gameManager():
    def __init__(self):
        self.currgames     = {}

    def addGame(self,gametoAdd, gameID):
        self.currgames[gameID] = gametoAdd

    def destoryGame(self,gameID):
        gametoDestory = self.currgames[gameID]
        self.currgames.pop(gameID)
        del gametoDestory

    def move(self,gameID, snakeID,move):
        snakes = self.currgames[gameID].getSnakes()
        snakes[snakeID].setMove(move)

    def startGame(self, gameID):
        self.currgames[gameID].setRunning(True)

    def addPlayer(self, gameID):
        game = self.currgames[gameID]
        playerNum = game.getPlayersJoined()
        snakeID = game.getStartSnakeID(playerNum)
        game.addPlayer()
        return playerNum,snakeID

    def getCurrGames(self):
        return self.currgames

    def updateGame(self,game):
        gameOver      = False
        return_winner  = ''

        deadSnakes = []
        deadSnakes.extend(game.checkWalls())
        game.checkFood()
        deadSnakes.extend(game.checkHeadOnCollisions())
        deadSnakes.extend(game.checkCollisions())

        if len(deadSnakes) > 0:
            game.addDeadSnake(deadSnakes)
            curr_dead = game.getDeadSnakes()
            if (len(curr_dead) >= (constants.PLAYERS - 1)):
                gameOver = True
                allsnakes = game.getAllSnakes()
                winner = list(set(allsnakes) - set(curr_dead))
                winnerstring = ''
                if (len(winner) > 0):
                    winnerstring = winner[0]
                else:
                    winnerstring = 'tie'
                return_winner = {'winner': winnerstring}


        return_dict = {}
        snakeList = []
        snakes = game.getSnakes()
        for snakeID in snakes:
            snake = snakes[snakeID]
            colour = '#' + snake.getcolour()
            snakePosition = snake.getPos()
            snakeList.append({'snakeID': snakeID, 'snakePosition': snakePosition, 'snakeColour': colour})
        food = game.getFood()
        return_dict['snakes'] = snakeList
        return_dict['food'] = food

        return gameOver, return_winner, return_dict