import random
from random import randrange
import string
import constants


# 0   1   2   3   4   5   6   7   8   9
# 10  11  12  13  14  15  16  17  18  19
# 20  21  22  23  24  25  26  27  28  29
# 30  31  32  33  34  35  36  37  38  39
# 40  41  42  43  44  45  46  47  48  49
# 50  51  52  53  54  55  56  57  58  59
# 60  61  62  63  64  65  66  67  68  69
# 70  71  72  73  74  75  76  77  78  79
# 80  81  82  83  84  85  86  87  88  89
# 90  91  92  93  94  95  96  97  98  99

# Legend
# cord(x,y)

# creatSnakeID()
# This function creates a random 4 char string of digitis and uppercase letters
# Returns the len 4 string
def creatSnakeID():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

# creatGameID()
# This function creates a random 4 char string of digitis and uppercase letters
# Returns the len 4 string
def creatGameID():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

# checkWalls()
# Params
# - game game which is a game class instance
# This function checks to see if a snakes move is valid, and won't result in it going out of bounds.
# Returns a list of snakes that went out of bounds this turn to remove them from the game.
def checkWalls(game):
    snakes = game.getSnakes()
    snakeOutofBounds = []
    for snakeID in snakes:
        snake         = snakes[snakeID]
        move          = snake.getMove()
        snakePosition = snake.getPos()
        snakeHead     = snakePosition[0]

        if(move == 'R'):
            if(snakeHead['x'] + 1) > 9:
                snakeOutofBounds.append(snakeID)
            else:
                y = snakeHead['y']
                x = snakeHead['x'] + 1
                snakePosition.insert(0, {'x':x,'y':y})


        if(move == 'L'):
            if(snakeHead['x'] - 1) < 0:
                snakeOutofBounds.append(snakeID)
            else:
                y = snakeHead['y']
                x = snakeHead['x'] - 1
                snakePosition.insert(0, {'x':x,'y':y})


        if(move == 'D'):
            if(snakeHead['y'] + 1) > 9:
                snakeOutofBounds.append(snakeID)
            else:
                y = snakeHead['y'] + 1
                x = snakeHead['x']
                snakePosition.insert(0, {'x':x,'y':y})


        if(move == 'U'):
            if(snakeHead['y'] - 1) < 0:
                snakeOutofBounds.append(snakeID)
            else:
                y = snakeHead['y'] - 1
                x = snakeHead['x']
                snakePosition.insert(0, {'x':x,'y':y})

        del snakePosition[-1]
        snake.setPos(snakePosition)

    return snakeOutofBounds

# TODO: Checks if there was a collision, if it was head on head who won.
def checkCollisions(game):
    return 0

class snake:
    def __init__(self, position = [{'x':0,'y':0}]):
        self.snakeID    = creatSnakeID()
        self.position   = position
        self.move       = 'D'
        self.isAlive    = True
        self.colour     = '#9d32a8'
        self.randomColour()


    def getID(self):
        return self.snakeID

    def getLength(self):
        return len(self.position)

    def getMove(self):
        return self.move

    def setMove(self, move):
        self.move = move

    def getPos(self):
        return self.position

    def setPos(self,position):
        self.position = position

    def getcolour(self):
        return self.colour

    def setcolour(self, colour):
        self.colour = colour

    def randomColour(self):
        self.colour = "%06x" % random.randint(0, 0xFFFFFF)

class game():
    def __init__(self):
        self.gameID    = creatGameID()
        self.snakes    = {}
        self.snakeList = []
        self.initSnakes()
        self.playersJoined = 1
        self.running = False

    def initSnakes(self):
        for x in range(constants.PLAYERS):
            snakeCopy         = snake([{'x':randrange(10),'y':randrange(10)}])
            ID                = snakeCopy.getID()
            self.snakes[ID]   = snakeCopy
            self.snakeList.append(ID)

    def getSnakes(self):
        return self.snakes

    def getStartSnakeID(self,value):
        return self.snakeList[value]

    def getPlayersJoined(self):
        return self.playersJoined

    def addPlayer(self):
        self.playersJoined = self.playersJoined + 1

    def setRunning(self, bool):
        self.running = bool

    def getRunning(self):
        return self.running

    def getID(self):
        return self.gameID

    def checkWalls(self):
        return checkWalls(self)

# TODO: impplement a board class that takes care of food generation
class board():
    def __int__(self):
        self.state = 0
    def getBoard(self):
        print(self.state)

    def generateFood(self):
        return 0