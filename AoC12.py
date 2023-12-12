from functools import lru_cache
DEBUG = False
Q = "?"
OPERATIONAL = "."
DAMAGED = "#"


def fit_row(candidate):
    this_row = candidate[0].split(OPERATIONAL)
    flag = True
    script = candidate[1]
    this_row_shape = [len(x) for x in this_row]
    this_row_shape = tuple(filter(lambda x: x>0, this_row_shape))
    return this_row_shape == script


def recur_fit(row):
    if Q not in row[0]:
        return fit_row(row)
    Q_spot = row[0].find(Q)
    options = [row[0][:Q_spot]+DAMAGED+row[0][Q_spot+1:],
               row[0][:Q_spot]+OPERATIONAL+row[0][Q_spot+1:]]
    answer = 0
    for option in options:
        answer += recur_fit([option, row[1]])
    return answer


import re
import functools as ft

def possible_placements(condition, spring):
    for m in re.finditer(rf'(?=([^\.]{{{spring}}}[^#]))', condition):
        i = m.span(1)[0]
        if '#' in condition[:i]:
            break
        yield condition[i + spring + 1:]

@ft.cache
def count_placements(condition, springs):
    if not springs:
        return '#' not in condition
    first_spring, rest_springs = springs[0], springs[1:]
    return sum(count_placements(rest_condition, rest_springs)
                  for rest_condition
                  in possible_placements(condition, first_spring))

def day12p2():
    with open(file) as f:
        lines = [(f'.{"?".join([condition] * 5)}.',
                  tuple(map(int, springs.split(','))) * 5)
                 for condition, springs
                 in (line.strip().split() for line in f)]
        print(lines)
    res = sum(count_placements(condition, springs) for condition, springs in lines)
    print(res)


if __name__ == '__main__':
    if DEBUG:
        file = "data/example1.txt"
    else:
        file = "data/puzzle.txt"
    with open(file, "r") as f:
        data_string = f.read()
    data_string = data_string.split("\n")
    data_list = [x.split(" ") for x in data_string]
    for row in data_list:
        row[1] = tuple(map(int, row[1].split(",")))
    print(data_list)
    # print(fit_row(data_list[1]))
    print(recur_fit(data_list[0]))
    answer = 0
    for row in data_list:
        answer += recur_fit(row)
    print(answer)
    day12p2()


