from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import functools as ft
import difflib

DEBUG = False
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
    return flip


def string_hash_job(string,pos):
    return string[:pos] + HASH + string[pos+1:]


def make_and_test_options(grid, options):
    hits = [[],[]]
    for option in options:
        y = option[0]
        this_grid = grid.copy()
        this_grid[y] = this_grid[option[1]]
        print(option)
        pprint(this_grid)
        if option[0] == 0:
            hits[0].append(option[1])
        elif option[0] == len(this_grid) - 1:
            hits[1].append(option[1])
        elif option[1] == 0:
            hits[0].append(option[0])
        elif option[1] == len(this_grid) - 1:
            hits[1].append(option[0])
        else:
            hits = find_matches(this_grid, hits)
        # print(hits)
        val = test_matches(this_grid, hits, False)
        if val is not None:
            return val, hits
    return None, hits


def find_smudge_stage2(grid, possibles):
    options = []
    for option in possibles:
        a, b = option
        row_a = grid[a]
        # print (a, row_a)
        row_b = grid[b]
        diff_count = 0
        diff_locale = 0
        diff = difflib.ndiff(row_a, row_b)
        pos = 0
        for k, s in enumerate(diff):
            # print(s[0], row_a[k], row_b[k])
            if s[0] == '-':
                diff_count += 1
                diff_locale = pos
            if diff_count == 2:
                break
            pos += 1
        if diff_count == 1 and (a + b) % 2 == 1 :
            # print(row_a, row_b, diff_locale)
            options.append((a, b, diff_locale))
        # print(a, b, row_a, row_b, diff_count)
    return options


def find_smudge_stage1(grid):
    counts = []
    for row in grid:
        counts.append(row.count(HASH))
    # print(counts)
    possible_rows = set()
    for x, count_a in enumerate(counts):
        for y, count_b in enumerate(counts):
            if count_a == count_b - 1:
                possible_rows.add((x,y))
    # print(possible_rows)
    # for a in grid:
    #     for b in grid:
    #         diff = difflib.ndiff(a, b)
    #         print(diff.__next__(), a, b)
    return possible_rows


def find_matches(grid, hits=None):
    candidates_coord = [0, len(grid)-1]
    candidates_row = [grid[0], grid[-1]]
    hits = hits or [[],[]]
    for i in range(2):
        candidate = candidates_row[i]
        for y, row in enumerate(grid):
            if row == candidate and y != candidates_coord[i]:
                hits[i].append(y)
    return hits


def test_matches(local_grid, hits, debug = False):
    front_hits = hits[0]
    back_hits = hits[1]
    flag = False
    debug_data = []
    for hit in front_hits:
        flag = True
        mirror_width = (hit+1) // 2
        if debug:
            print(hit, mirror_width )
            # print([(i, local_grid[i] == local_grid[hit - i], local_grid[i], local_grid[hit - i]) for i in range(mirror_width + 1)])
            pprint(local_grid)
        if all(
                [local_grid[i] == local_grid[hit - i] for i in range(mirror_width + 1)]
        ):
            return mirror_width
        elif debug:
            print("No match,", [(i, local_grid[i] == local_grid[hit - i], local_grid[i], local_grid[hit - i]) for i in range(mirror_width + 1)])
    for hit in back_hits:
        flag = True
        # print(hit, hit+len(grid)//2, len(grid))
        mirror_width = (len(local_grid) - hit) // 2
        if debug:
            print("\n\n",hit, mirror_width )
            # print("\n".join(grid))
            pprint(local_grid)
        if all(
            [local_grid[hit + i] == local_grid[-(i + 1)] for i in range(mirror_width)]
        ):
            # print("Winner!",hit+len(grid)//2)
            # winner
            return hit+mirror_width
    if flag and debug:
        print("\n".join(local_grid), "\n", hits)
        # print("\n\n".join(debug_data))
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
    answer2 = 0
    for grid in data_list:
        grid_val = test_matches(grid, find_matches(grid))
        if grid_val is not None:
            answer += 100 * grid_val
        else:
            f_grid = flipperooni(grid)
            answer += test_matches(f_grid, find_matches(f_grid), False) or 0
            # input()
        possibles = find_smudge_stage1(grid)
        options = find_smudge_stage2(grid, possibles)
        grid_val_2, hits = make_and_test_options(grid, options)
        if grid_val_2 is not None:
            answer2 += 100 * grid_val_2
        else:
            possibles = find_smudge_stage1(f_grid)
            options = find_smudge_stage2(f_grid, possibles)
            grid_val_2, f_hits = make_and_test_options(f_grid, options)
            print(grid_val_2, f_hits, hits)
            pprint(f_grid)
            pprint(grid)
            answer2 += grid_val_2

    print(answer)
    print("Second:",answer2)

    # Need to consider idea that smudge is in a throwaway row/column

