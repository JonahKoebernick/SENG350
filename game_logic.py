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
            y = snakeHead['y']
            x = snakeHead['x'] + 1
            snakePosition.insert(0, {'x':x,'y':y})


        if(move == 'L'):
            if(snakeHead['x'] - 1) < 0:
                snakeOutofBounds.append(snakeID)
            y = snakeHead['y']
            x = snakeHead['x'] - 1
            snakePosition.insert(0, {'x':x,'y':y})


        if(move == 'D'):
            if(snakeHead['y'] + 1) > 9:
                snakeOutofBounds.append(snakeID)
            y = snakeHead['y'] + 1
            x = snakeHead['x']
            snakePosition.insert(0, {'x':x,'y':y})


        if(move == 'U'):
            if(snakeHead['y'] - 1) < 0:
                snakeOutofBounds.append(snakeID)
            y = snakeHead['y'] - 1
            x = snakeHead['x']
            snakePosition.insert(0, {'x':x,'y':y})

        snake.setPos(snakePosition)
    return snakeOutofBounds

# checkFood()
# Params
# - game game which is a game class instance
# This function checks to see if a snakes is on food.
# It contains the growing mechanics for the snakes
def checkFood(game):
    snakes = game.getSnakes()
    food   = game.getFood()

    for snakeID in snakes:
        snake         = snakes[snakeID]
        snakePosition = snake.getPos()
        snakeHead = snakePosition[0]


        # If it is on a food block, it grows by one. So the tail isn't deleted.
        # And we need to generate a new food block
        if (snakeHead['x'] == food['x']) and (snakeHead['y'] == food['y']):
            game.generateFood()

        # If it isn't on food, delete it's tail
        else:
            del snakePosition[-1]
            snake.setPos(snakePosition)

# checkHeadOnCollision()
# Params
# - game game which is a game class instance
# This function checks to see if there was a head on head collisions
# returns a list of deadsnakes
def checkHeadOnCollision(game):
    snakes = game.getSnakes()
    deadSnakes = []

    for snakeID in snakes:
        snake         = snakes[snakeID]
        snakePosition = snake.getPos()
        snakeHead = snakePosition[0]
        length    = len(snakePosition)

        for snakeIDtoCheck in snakes:
            snaketoCheck = snakes[snakeIDtoCheck]
            snakePositiontoCheck = snaketoCheck.getPos()
            snakeHeadtoCheck = snakePositiontoCheck[0]
            lengthtoCheck = len(snakePositiontoCheck)

            if(snakeID != snakeIDtoCheck):
                if snakeHead == snakeHeadtoCheck:
                    if(length > lengthtoCheck):
                        deadSnakes.append(snakeIDtoCheck)
                    if(length == lengthtoCheck):
                        deadSnakes.append(snakeIDtoCheck)
                        deadSnakes.append(snakeID)
                    if(length < lengthtoCheck):
                        deadSnakes.append(snakeID)

    return list(set(deadSnakes))

# checkCollision()
# Params
# - game game which is a game class instance
# This function checks to see if there was a head on body collision
# returns a list of deadsnakes
def checkCollision(game):
    snakes = game.getSnakes()
    deadSnakes = []

    for snakeID in snakes:
        snake         = snakes[snakeID]
        snakePosition = snake.getPos()
        snakeHead = snakePosition[0]

        for snakeIDtoCheck in snakes:
            snaketoCheck = snakes[snakeIDtoCheck]
            snakePositiontoCheck = snaketoCheck.getPos()

            for j in range(1,len(snakePositiontoCheck)):
                if(snakeHead['y'] == snakePositiontoCheck[j]['y']) and (snakeHead['x'] == snakePositiontoCheck[j]['x']):
                    deadSnakes.append(snakeID)

    return list(set(deadSnakes))

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


class board():
    def __int__(self):
        self.food = {'x':0,'y':0}

    def getFood(self):
        return self.food

    def generateFood(self,snakes):
        x = randrange(10)
        y = randrange(10)
        xlist = []
        ylist = []
        for snakeID in snakes:
            snake = snakes[snakeID]
            snakePosition = snake.getPos()
            for pos in snakePosition:
                xlist.append(pos['x'])
                ylist.append(pos['y'])
        while x in xlist:
            x = randrange(10)

        while y in ylist:
            y = randrange(10)
        self.food = {'x':x,'y':y}

class game():
    def __init__(self):
        self.gameID    = creatGameID()
        self.snakes    = {}
        self.snakeList = []
        self.deadSnakes = []
        self.initSnakes()
        self.playersJoined = 1
        self.running = False
        self.board = board()
        self.generateFood()

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

    def checkHeadOnCollisions(self):
        return checkHeadOnCollision(self)

    def checkCollisions(self):
        return checkCollision(self)

    def checkFood(self):
        checkFood(self)

    def getFood(self):
        return self.board.getFood()

    def generateFood(self):
        self.board.generateFood(self.snakes)

    def addDeadSnake(self, snake):
        self.deadSnakes = self.deadSnakes + snake

    def getDeadSnakes(self):
        return self.deadSnakes

    def getAllSnakes(self):
        return self.snakeList

