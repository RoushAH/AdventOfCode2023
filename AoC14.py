from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import functools as ft
import difflib

DEBUG = True
ROLLER = "O"
HASH = "#"
BLANK = "."


def flipperooni(grid):
    # print(grid)
    flip = [
        "".join([
            grid[y][x] for y in range(len(grid))
        ]) for x in range(len(grid[0]))
    ]
    # flip = []
    # for x in range(len(grid[0])):
    #     print("x=",x)
    #     row = []
    #     for y in range(len(grid)):
    #         print("y=",y)
    #         row.append(grid[y][x])
    #     flip.append(row)
    return flip


def pprint(list):
    print()
    for number, row in enumerate(list):
        disp = f"{number:02d}: "
        for char in row:
            disp += str(char)
        print(disp)


def find_rollers(column):
    rollers = []
    for pos, char in enumerate(column):
        if char == ROLLER:
            rollers.append(pos)

    return rollers


def promote(column):
    max_score = len(column)
    score = 0
    # print(column)
    current = 0
    final = 0
    rollers = find_rollers(column)
    # print(rollers)
    for current in rollers:
        # print(current)
        for pos in range(current-1, -1, -1):
            # print(pos, column[pos])
            if column[pos] != BLANK:
                final = pos + 1
                break
        if final != current:
            column = column[:final] + ROLLER + column[final:current] + column[current+1:]
        score += max_score - final
    return score, column


if __name__ == '__main__':
    if DEBUG:
        file = "data/example2.txt"
    else:
        file = "data/puzzle2.txt"
    with open(file, "r") as f:
        data_string = f.read()
    data_string = data_string.split("\n")
    # pprint(data_string)
    data_cols = flipperooni(data_string)
    result = 0
    for col in data_cols:
        points, col = promote(col)
        # print(points, col)
        result += points
    print(result)