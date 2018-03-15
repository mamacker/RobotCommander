#!/usr/bin/python

# This is meant to be used with the "Robot Commander" Alexa Skill and
# a Raspberry PI Sense Hat
#
# Try the Robot Commander Skill, then, get your Robot Commander ID by saying:
# "Alexa, ask Robot Commander for my ID"
# - or -
# If you are already in Robot Commander say:
# "What is my Commander ID"
# Alexa will respond with a 6 character code.  Put that code in the
# ID slot below, and what your robots progress in real time IOT.

from sense_hat import SenseHat
import requests
import json
import time

last_request_time = 0
board = None
position = None
max_size = 0

def get_board(id):
    global last_request_time
    global board
    global position
    global max_size
    changed = False
    # Only fetch the board every three seconds
    if time.time() - last_request_time > 3:
        last_request_time = time.time()

        r = requests.get('https://api.robotcommander.io/board?id=' + str(id))
        if len(r.text) == 0:
            print "Invalid board id.  Say, 'Alexa, ask robot commander for my ID' use that string."
            return None, None, None, False
        board_data = r.json()
        board_values = board_data["game"]
        json_data = json.loads(board_values)

        board_raw = json_data["board"]
        board = []

        # First build out the max board.
        for x in range(10):
            board.append([])
            for y in range(20):
                board[x].append(0)

        # Parse the data in the board return value.
        for x in range(len(board_raw)):
            if board_raw[x] is not None:
                for y in range(len(board_raw[x])):
                    if board_raw[x][y] is not None:
                        if board_raw[x][y].get("safe") is not None:
                                if board_raw[x][y].get("safe"):
                                    if board_raw[x][y].get("visited") is True:
                                        board[board_raw[x][y].get("x")][board_raw[x][y].get("y")] = 1
                                else:
                                    board[board_raw[x][y].get("x")][board_raw[x][y].get("y")] = -1
                        if max_size < board_raw[x][y].get("y"):
                            max_size = board_raw[x][y].get("y")

        # Trim the board to the maximum y value seen.
        for j in range(len(board)):
            for k in range(max_size, 20):
                board[j][k] = 1

        position = [json_data["position"].get("x"), json_data["position"].get("y")];
        changed = True
    return (board, position, max_size, changed)

sense = SenseHat()
sense.clear()

while True:
    board, position, level, changed = get_board('qmda82')
    shift = 1
    if changed is True:
        sense.clear()
        for x in range(len(board)):
            shift_x = x - shift
            if shift_x > 7 or shift_x < 0:
                continue
            for y in range(len(board[x])):
                if y > 7:
                    continue
                if board[x][y] == 1:
                    sense.set_pixel(shift_x, 7 - y, [0, 255, 0])
                elif board[x][y] == -1:
                    sense.set_pixel(shift_x, 7 - y, [255, 0, 0])
                elif board[x][y] == 0:
                    sense.set_pixel(shift_x, 7 - y, [0, 0, 0])

        sense.set_pixel(position[0] - shift, 7 - position[1], [0, 0, 255])
    time.sleep(1)

