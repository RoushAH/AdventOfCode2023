import pprint

DEBUG = True
circuit = []
U = "U"
D = "D"
L = "L"
R = "R"
EMPTY = "."
HASH = "#"
moves = {
    U: (0, -1),
    D: (0, 1),
    L: (-1, 0),
    R: (1, 0)
}
y_lims = [0,0]
x_lims = [0,0]
grid = []


def show_circuit():
    for spot in circuit:
        grid[spot[1]-y_lims[0]][spot[0]-x_lims[0]] = HASH
    # for row in grid:
    #     print("".join(row))


def count_row(y, row):
    print("".join(row))
    disp_row = ""
    dig = False
    count = 0
    active = False
    for x, elem in enumerate(row):
        if [x, y] in circuit:
            disp_row += HASH
            count += 1
            if not active:
                active = True
                dig = not dig
        elif dig:
            count += 1
            disp_row += HASH
            active = False
        else:
            disp_row += EMPTY
            active = False
    print(disp_row)
    return count


def follow_circuit(data_list):
    loc = [0, 0]
    # circuit.append(loc)
    for instruction in data_list:
        dir, steps, _ = instruction
        for step in range(steps):
            print(moves[dir], loc)
            loc[0] += moves[dir][0]
            loc[1] += moves[dir][1]
            x_lims[0] = min(x_lims[0], loc[0])
            y_lims[0] = min(y_lims[0], loc[1])
            x_lims[1] = max(x_lims[1], loc[0])
            y_lims[1] = max(y_lims[1], loc[1])
            circuit.append(loc.copy())


if __name__ == '__main__':
    if DEBUG:
        file = "data/example1.txt"
    else:
        file = "data/puzzle.txt"
    with open(file, "r") as f:
        data_string = f.read()
    data_string = data_string.split("\n")
    data_list = [row.split() for row in data_string]
    for row in data_list:
        row[1] = int(row[1])
    # print(data_list)
    follow_circuit(data_list)
    print(circuit)
    grid = [[EMPTY for x in range(x_lims[1] - x_lims[0] + 3)] for y in range(y_lims[1] - y_lims[0] + 3)]
    show_circuit()
    answer = 0
    for y, row in enumerate(grid):
        answer += count_row(y, row)
    print(answer)
