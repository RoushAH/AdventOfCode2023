from functools import reduce
DEBUG = False
sequences = []


def next_val_recurse(vals):
    # print(vals)
    if all(v ==0 for v in vals):
        return 0
    start = vals[0]
    reduced = []
    for val in vals[1:]:
        reduced.append(val-start)
        start = val
    print(reduced)
    next_val = vals[-1] + next_val_recurse(reduced)
    print(next_val)
    return next_val


def first_val_recurse(vals):
    # print(vals)
    if all(v ==0 for v in vals):
        return 0
    start = vals[0]
    reduced = []
    for val in vals[1:]:
        reduced.append(val-start)
        start = val
    # print(reduced)
    first_val = vals[0] - first_val_recurse(reduced)
    print(first_val, [first_val]+reduced)
    return first_val


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if DEBUG:
        file = "data/example1.txt"
    else:
        file = "data/puzzle.txt"
    with open(file, "r") as f:
        data_string = f.read()
    data_list = data_string.split("\n")
    data_list = [list(map(int, x.split())) for x in data_list]
    print(data_list)
    sum = 0
    for row in data_list:
        sum += first_val_recurse(row)
    print(sum)
