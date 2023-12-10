import time
DEBUG = True
PIPES = {
    "F": ("D", "R"),
    "L": ("R", "U"),
    "J": ("L", "U"),
    "7": ("D", "L"),
    "-": ("L", "R"),
    "|": ("D", "U")
}
data_list = []
active_paths = []
path_length = 0



def find_start():
    for row, string in enumerate(data_list):
        if "S" in string:
            return (row, string.index("S"))


def find_start_shape(dirs):
    dirs = tuple(dirs)
    for shape, tup in PIPES.items():
        print(tup, dirs)
        if tup == dirs:
            return shape


def next_step():
    global path_length
    for pos, start in enumerate(active_paths):
        pipe = data_list[start[0]][start[1]]
        choices = PIPES[pipe]
        if "U" in choices and data_list[start[0]-1][start[1]] in ["7", "|", "F"]:
            active_paths[pos] =  (start[0]-1, start[1])
        if "R" in choices and data_list[start[0]][start[1]+1] in ["7", "-", "J"]:
            active_paths[pos] = (start[0], start[1]+1)
        if "D" in choices and data_list[start[0]+1][start[1]] in ["L", "|", "J"]:
            active_paths[pos] = (start[0]+1, start[1])
        if "L" in choices and data_list[start[0]][start[1]-1] in ["F", "-", "L"]:
            active_paths[pos] = (start[0], start[1]-1)
        data_list[start[0]][start[1]] = "S"
    path_length += 1



if __name__ == '__main__':
    if DEBUG:
        file = "data/example3.txt"
    else:
        file = "data/puzzle.txt"
    with open(file, "r") as f:
        data_string = f.read()
    data_list = data_string.split("\n")
    data_list = ["."*len(data_list[0])]+data_list+["."*len(data_list[0])]
    data_list = ["." + row + "." for row in data_list]
    data_list = [list(row) for row in data_list]
    print(data_list)
    start = find_start()
    start_shapes = []
    if data_list[start[0]+1][start[1]] in ["L", "|", "J"]:
        active_paths.append((start[0]+1, start[1]))
        start_shapes.append("D")
    if data_list[start[0]][start[1]-1] in ["F", "-", "L"]:
        active_paths.append((start[0], start[1]-1))
        start_shapes.append("L")
    if data_list[start[0]][start[1]+1] in ["7", "-", "J"]:
        active_paths.append((start[0], start[1]+1))
        start_shapes.append("R")
    if data_list[start[0]-1][start[1]] in ["7", "|", "F"]:
        active_paths.append((start[0]-1, start[1]))
        start_shapes.append("U")
    path_length += 1
    print(active_paths, path_length)
    print(start_shapes)
    start_shape = find_start_shape(start_shapes)
    # while active_paths[0] != active_paths[1]:
    #     next_step()
    #     print(active_paths, path_length)
    #     # time.sleep(.5)
    # print(active_paths, path_length)
    data_list[start[0]][start[1]] = start_shape

# Press the green button in the gutter to run the script.
