from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import functools as ft

DEBUG = True
HASH = "#"


def pprint(list):
    print()
    for number, row in enumerate(list):
        disp = f"{number:02d}: "
        for char in row:
            disp += str(char)
        print(disp)


def flipperooni(grid):
    flip = [
        "".join([
            grid[y][x] for y in range(len(grid))
        ]) for x in range(len(grid[0]))
    ]
    # print("\n".join(grid))
    # print("\n\n")
    # print("\n".join(flip))
    return flip


def find_matches(grid):
    candidates_coord = [0, len(grid)-1]
    candidates_row = [grid[0], grid[-1]]
    hits = [[],[]]
    for i in range(2):
        candidate = candidates_row[i]
        for y, row in enumerate(grid):
            if row == candidate and y != candidates_coord[i]:
                hits[i].append(y)
    return hits


def test_matches(grid, hits, debug = False):
    front_hits = hits[0]
    back_hits = hits[1]
    flag = False
    debug_data = []
    for hit in front_hits:
        flag = True
        mirror_width = (hit+1) // 2
        if debug:
            print(hit, mirror_width )
            # print("\n".join(grid))
            pprint(grid)
        if all(
                [grid[i] == grid[hit-i] for i in range(mirror_width+1)]
                # if exactly 1 False, this is the winner of part 2...
        ):
            return mirror_width
    for hit in back_hits:
        flag = True
        # print(hit, hit+len(grid)//2, len(grid))
        mirror_width = (len(grid) - hit)//2
        if debug:
            print("\n\n",hit, mirror_width )
            # print("\n".join(grid))
            pprint(grid)
        if all(
            [grid[hit + i] == grid[-(i+1)] for i in range(mirror_width)]
        ):
            # print("Winner!",hit+len(grid)//2)
            # winner
            return hit+mirror_width
    if flag and debug:
        print("\n".join(grid), "\n", hits)
        print("\n\n".join(debug_data))
        input()
    pass


if __name__ == '__main__':
    if DEBUG:
        file = "data/example1.txt"
    else:
        file = "data/puzzle.txt"
    with open(file, "r") as f:
        data_string = f.read()
    data_string = data_string.split("\n\n")
    # print(data_string)
    data_list = [row.split("\n") for row in data_string]
    # print(test_matches(data_list[1], find_matches(data_list[1])))
    # print(find_matches(data_list[1]))
    answer = 0
    for grid in data_list:
        grid_val = test_matches(grid, find_matches(grid))
        if grid_val is not None:
            answer += 100 * grid_val
        else:
            f_grid = flipperooni(grid)
            answer += test_matches(f_grid, find_matches(f_grid), False) or 0
            # input()
        find_smudge(grid)
    print(answer)
