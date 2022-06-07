from keras.models import load_model
import cv2
import numpy as np
from random import choice

userScore = 0
pcScore = 0
tieScore = 0

REV_CLASS_MAP = {
    0: "rock",
    1: "paper",
    2: "scissors",
    3: "none",
    4: "start",
    5: "end"
}
gameStarted = 0

def mapper(val):
    return REV_CLASS_MAP[val]


def calculate_winner(move1, move2):
    if move1 == move2:
        return "Tie"

    if move1 == "rock":
        if move2 == "scissors":
            return "User"
        if move2 == "paper":
            return "Computer"

    if move1 == "paper":
        if move2 == "rock":
            return "User"
        if move2 == "scissors":
            return "Computer"

    if move1 == "scissors":
        if move2 == "paper":
            return "User"
        if move2 == "rock":
            return "Computer"
    return 'Waiting...'

def loadGame(game):
    font = game.FONT_HERSHEY_SIMPLEX
    game.putText(frame, "Your Move: " + user_move_name,
                (50, 50), font, 1.2, (255, 255, 255), 2, game.LINE_AA)
    game.putText(frame, "Computer's Move: " + computer_move_name,
                (750, 50), font, 1.2, (255, 255, 255), 2, game.LINE_AA)
    game.putText(frame, "Winner: " + winner,
                (400, 600), font, 2, (0, 0, 255), 4, game.LINE_AA)
    game.putText(frame, "Score: " + str(userScore),
                (150, 700), font, 2, (0, 0, 255), 4, game.LINE_AA)
    game.putText(frame, "Score: " + str(pcScore),
                (850, 700), font, 2, (0, 0, 255), 4, game.LINE_AA)
    game.putText(frame, "Ties: " + str(tieScore),
                (500, 700), font, 2, (0, 0, 255), 4, game.LINE_AA)

def getUserMove(model):
    pred = model.predict(np.array([img]))
    move_code = np.argmax(pred[0])
    return mapper(move_code)


model = load_model("rock-paper-scissors-model.h5")

cap = cv2.VideoCapture(0)

def make_1080p():
    cap.set(3, 1920)
    cap.set(4, 1060)

def make_720p():
    cap.set(3, 1280)
    cap.set(4, 720)

prev_move = None
computer_move_name = 'none'
winner = 'Waiting...'
    

while True:
    k = cv2.waitKey(10)
    make_720p()
    ret, frame = cap.read()
    if not ret:
        continue

    # rectangle for user to play
    cv2.rectangle(frame, (100, 100), (500, 500), (255, 255, 255), 2)
    # rectangle for computer to play
    cv2.rectangle(frame, (800, 100), (1200, 500), (255, 255, 255), 2)

    # extract the region of image within the user rectangle
    roi = frame[100:500, 100:500]
    img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (227, 227))

    # predict the move made
    user_move_name = getUserMove(model)

    # predict the winner (human vs computer)
    if prev_move != user_move_name:
        if user_move_name != "none":
            if user_move_name == "start" and gameStarted == 0:
                gameStarted = 1
                # prev_move = None
            if gameStarted == 1:
                if k == ord('r'):
                    computer_move_name = choice(['rock', 'paper', 'scissors'])
                    winner = calculate_winner(user_move_name, computer_move_name)
                    if (winner == 'User'):
                        userScore += 1
                        gameStarted = 0
                    elif (winner == 'Computer'):
                        pcScore += 1
                        gameStarted = 0
                    else:
                        tieScore += 1
                        gameStarted = 0
                k = ''
        else:
            computer_move_name = "none"
            winner = "Waiting..."
    prev_move = user_move_name

    # display the information
    loadGame(cv2)

    if computer_move_name != "none":
        icon = cv2.imread(
            "images/{}.png".format(computer_move_name))
        icon = cv2.resize(icon, (400, 400))
        frame[100:500, 800:1200] = icon

    cv2.imshow("Rock Paper Scissors", frame)

    # if user_move_name == 'end':
    #     print('Because of this')
    #     break
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print('GAME ENDED!')
