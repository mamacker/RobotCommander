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

import time
import robotio
from sense_hat import SenseHat
sense = SenseHat()
sense.clear()

while True:
    board, position, level, changed = robotio.get_board('qmda82')
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

