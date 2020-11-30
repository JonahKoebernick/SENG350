from flask import  Flask,send_from_directory, jsonify, make_response, request ,redirect, abort, render_template, g, send_file
from flask_socketio import SocketIO, emit, join_room, leave_room
from random import randrange
from apscheduler.schedulers.background import BackgroundScheduler
import game_logic
import constants
import time
import sys

# Boiler plate
app = Flask(__name__)
socketio = SocketIO(app)

# Dictonary that contains all the games currently in progress
gameManager = game_logic.gameManager()



def sensor():
    global  gameManager
    currgames = gameManager.getCurrGames()
    keylist = list(currgames)
    for gameID in keylist:
        game = currgames[gameID]
        if(game.getRunning() == True):
            gameOver, return_winner, return_dict = gameManager.updateGame(game)

            if(gameOver):
                socketio.emit('gameOver', return_winner, room=gameID)
                gameManager.destoryGame(gameID)
            else:
                socketio.emit('boardState', return_dict, room=gameID)


# The Scheduler that times the games, alerting this value sets the moves per Second
sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',seconds=2)
sched.start()


@socketio.on('hostGame')
def hostGame():
    # Initialize a new game and add it do the dictionary
    game      = game_logic.game()
    gameID    = game.getID()
    snakeID   = game.getStartSnakeID(0)
    gameManager.addGame(game, gameID)

    # Bind the User to the Specific
    # This is part of the subscribes publisher pattern.
    # The client subscribes to a gameID, and when that game is updated they are notified.
    join_room(gameID)

    # Send GameID and the SnakeID of the user
    return_dict = {}
    return_dict['gameID'] =  gameID
    return_dict['snakeID'] = snakeID
    socketio.emit('startInfo',return_dict)



@socketio.on('move')
def move(data):
    # Extract all the data
    gameID  = data['gameID']
    move    = data['move']
    snakeID = data['snakeID']

    # Get the dictonary of snakes and set the move
    gameManager.move(gameID, snakeID, move)



@socketio.on('startGame')
def startGame(data):
    # Extract data
    gameID = data['gameID']

    # Start the game
    gameManager.startGame(gameID)

@socketio.on('joinGame')
def joinGame(data):
    # Extract Data
    gameID    = data['gameID']


    # Add player to game instance
    playerNum, snakeID = gameManager.addPlayer(gameID)
    join_room(gameID)

    # Send GameID and the SnakeID of the user
    return_dict = {}
    return_dict['gameID'] =  gameID
    return_dict['snakeID'] = snakeID
    socketio.emit('gameInfo', return_dict)

    # If the room is full, alert the host they can start
    if (playerNum + 1) == constants.PLAYERS:
        socketio.emit('gameReady',room=gameID)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/stylesheet')
def stylesheet():
    return send_from_directory('/static/CSS/', 'main.css')

@app.route('/javascript')
def javascript():
    return send_from_directory('/static/js/', 'scripts.js')

if __name__ == '__main__':
    app.static_folder = 'static'
    app.run()