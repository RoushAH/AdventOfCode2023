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
    sum = 0
    for option in options:
        sum += recur_fit([option, row[1]])
    return sum


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
    sum = 0
    for row in data_list:
        sum += recur_fit(row)
    print(sum)
