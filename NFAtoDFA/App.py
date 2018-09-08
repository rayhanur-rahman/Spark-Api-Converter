import re, random, math

def move(state, input):

    if input == 'a':
        if state == 0:
            return 1
        if state == 1:
            return 1
        if state == 2:
            return 2
        if state == 3:
            return 3
        if state == 4:
            return 4
        if state == 5:
            return 5
        if state == 6:
            return 6
        if state == 7:
            return 7
        if state == 8:
            return 8
        if state == 9:
            return 9

    if input == 'b':
        if state == 0:
            return 0
        if state == 1:
            return 1
        if state == 2:
            return 2
        if state == 3:
            return 3
        if state == 4:
            return 5
        if state == 5:
            return 5
        if state == 6:
            return 6
        if state == 7:
            return 7
        if state == 8:
            return 8
        if state == 9:
            return 9

    if input == 'c':
        if state == 0:
            return 0
        if state == 1:
            return 1
        if state == 2:
            return 2
        if state == 3:
            return 3
        if state == 4:
            return 4
        if state == 5:
            return 5
        if state == 6:
            return 7
        if state == 7:
            return 7
        if state == 8:
            return 8
        if state == 9:
            return 9

    return None

def epsilonTransition(state):
    states = {
        0:[],
        1:[2,3,4,6,9],
        2:[3,4,6,9],
        4:[],
        5:[8,9,3,4,6],
        6:[],
        7:[8,9,3,4,6],
        8:[3,4,6,9],
        9:[]
    }

