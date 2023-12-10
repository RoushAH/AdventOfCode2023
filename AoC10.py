DEBUG = False
PIPES = {
    "F": ("D", "R"),
    "L": ("R", "U"),
    "J": ("L", "U"),
    "7": ("D", "L"),
    "-": ("L", "R"),
    "|": ("D", "U"),
}
EMPTY = "."
data_list = []
active_paths = []
path_length = 0
visited = []
winners = 0


def junk_pipe_scan(array):
    print(visited)
    answer = 0
    for y, row in enumerate(array):
        crossings = 0
        crosser = EMPTY
        for x, char in enumerate(row):
            if char == "|" and (y, x) in visited:
                crossings += 1
            elif char == "-" and (y, x) in visited:
                pass
            elif char == "F" and (y, x) in visited:
                crosser = "F"
            elif char == "7" and (y, x) in visited:
                if crosser == "L":
                    crossings += 1
                    crosser = EMPTY
            elif char == "L" and (y, x) in visited:
                crosser = "L"
            elif char == "J" and (y, x) in visited:
                if crosser == "F":
                    crossings += 1
                    crosser = EMPTY
            else:
                answer += crossings % 2
                array[y][x] = crossings
                # print((y, x),char)
                # check to see how many times the moat's been crossed
    return array, answer


def pprint(list, split=1):
    print()
    if split == 1:
        for number, row in enumerate(list):
            disp = f"{number:02d}: "
            for char in row:
                disp += str(char)
            print(disp)
    else:
        for number, row in enumerate(list):
            disp = f"{number:02d}: "
            if number % split == 0:
                for pos, char in enumerate(row):
                    if pos % split == 0:
                        disp += str(char)
                print(disp)


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
        visited.append(active_paths[pos])
    path_length += 1


if __name__ == '__main__':
    if DEBUG:
        file = "data/example5.txt"
    else:
        file = "data/puzzle.txt"
    with open(file, "r") as f:
        data_string = f.read()
    data_string = data_string.split("\n")
    data_list = [EMPTY*len(data_string[0])]+data_string+[EMPTY*len(data_string[0])]
    data_list = [EMPTY + row + EMPTY for row in data_list]
    data_list = [list(row) for row in data_list]
    # pprint(data_list)
    # pprint(corners_list)
    start = find_start()
    visited.append(start)
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
    visited += active_paths
    path_length += 1
    # print(active_paths, path_length)
    # print(start_shapes)
    start_shape = find_start_shape(start_shapes)
    while active_paths[0] != active_paths[1]:
        next_step()
        # print(active_paths, path_length)
        # time.sleep(.5)
    end = active_paths.pop()
    print(active_paths, path_length)
    print(visited)
    # pprint(data_list)
    data_list = [EMPTY*len(data_string[0])]+data_string+[EMPTY*len(data_string[0])]
    data_list = [EMPTY + row + EMPTY for row in data_list]
    data_list = [list(row) for row in data_list]
    data_list[start[0]][start[1]] = start_shape
    answer_list, answer = junk_pipe_scan(data_list)
    print(answer)

# Press the green button in the gutter to run the script.
