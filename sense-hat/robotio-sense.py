#!/usr/bin/python
#from sense_hat import SenseHat
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
        if len(r.raw()) == 0:
            print "Invalid board id.  Say, 'Alexa, ask robot commander for my ID' use that string."
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
                    found = False;
                    if board_raw[x][y] is not None:
                        if board_raw[x][y].get("visited") is not None:
                            if board_raw[x][y].get("visited") is True:
                                if board_raw[x][y].get("safe"):
                                    board[board_raw[x][y].get("x")][board_raw[x][y].get("y")] = 1
                                else:
                                    board[board_raw[x][y].get("x")][board_raw[x][y].get("y")] = -1
                            if max_size < board_raw[x][y].get("y"):
                                max_size = board_raw[x][y].get("y")

        # Trim the board to the maximum y value seen.
        for j in range(len(board)):
            board[j] = board[j][:max_size]

        position = [json_data["position"].get("x"), json_data["position"].get("y")];
        changed = True
    return (board, position, max_size, changed)

sense = SenseHat()
sense.clear()

while True:
    board, position, level, changed = get_board('qmda8df2')
    if changed is True:
        sense.clear()
        for x in range(board):
            for y in range(board[x]):
                if board[x][y] == 1:
                    sense.set_pixel(x, y, [0, 255, 0])
                elif board[x][y] == -1:
                    sense.set_pixel(x, y, [255, 0, 0])
                elif board[x][y] == 0:
                    sense.set_pixel(x, y, [0, 0, 0])

        sense.set_pixel(position[0], position[1])
    time.sleep(1)

