import time
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import functools as ft
import difflib

DEBUG = False
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
    return flip


def pprint(list):
    print()
    for number, row in enumerate(list):
        disp = f"{number:02d}: "
        for char in row:
            disp += str(char)
        print(disp)


def first_instance(scores_list, search_pattern):
    length = len(search_pattern)
    for i in range(len(scores_list)):
        if scores_list[i:i+length] == search_pattern:
            return i
    pass


def is_pattern(scores_list):
    for i in range(4, len(scores_list)//4):
        candidate = scores_list[-i:]
        remainder = scores_list[:-i]
        print(i)
        if remainder[-len(candidate):] == candidate:
            return candidate
    pass


def find_rollers(column):
    rollers = []
    for pos, char in enumerate(column):
        if char == ROLLER:
            rollers.append(pos)
    return rollers


def grid_score(box_plot):
    max_score = len(box_plot[0])
    score = 0
    for this_row in box_plot:
        these_rollers = find_rollers(this_row)
        score += max_score * len(these_rollers)
        score -= sum(these_rollers)
    return score


def cycle(grid):
    # north
    for x in range(len(grid[0])):
        col = "".join([
            grid[y][x] for y in range(len(grid))
        ])
        col = promote(col, False)
        for y, val in enumerate(col):
            grid[y][x] = val
    # west
    for y, row in enumerate(grid):
        str_row = "".join(row)
        str_row = promote(str_row, False)
        grid[y] = list(str_row)
    # pprint(grid)
    # south
    for x in range(len(grid[0])):
        col = "".join([
            grid[y][x] for y in range(len(grid)-1, -1, -1)
        ])
        col = promote(col, False)
        for i, val in enumerate(col):
            y = len(grid) - 1 - i
            grid[y][x] = val
    # east
    for y, row in enumerate(grid):
        str_row = "".join(row)[::-1]
        str_row = promote(str_row, False)[::-1]
        # print(str_row)
        grid[y] = list(str_row)
    # score the grid flipperooni
    score = grid_score(flipperooni(grid))
    return score, grid


def promote(column, r_score=True):
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
    if r_score:
        return score, column
    return column


if __name__ == '__main__':
    if DEBUG:
        file = "data/example2.txt"
    else:
        file = "data/puzzle2.txt"
    with open(file, "r") as f:
        data_string = f.read()
    data_string = data_string.split("\n")
    data_list = [[char for char in row] for row in data_string]
    # pprint(data_string)
    data_cols = flipperooni(data_string)
    result = 0
    new = []
    for col in data_cols:
        points, col = promote(col)
        # print(points, col)
        new.append(col)
        result += points
    print(result)
    # pprint(data_list)
    new_grid = data_list.copy()
    scores = []
    for i in range(300):
        score, new_grid = cycle(new_grid)
        scores.append(score)
    print(i, score)
    print(grid_score(new))
    pattern = is_pattern(scores)
    print(pattern)
    start = first_instance(scores, pattern)
    print(start)
    tgt = 1000000000
    answer = tgt - start - 1
    answer = answer % len(pattern)
    print(pattern[answer])
