DEBUG = False
MAP_ORDER = ("seed-to-soil",
             "soil-to-fertilizer",
             "fertilizer-to-water",
             "water-to-light",
             "light-to-temperature",
             "temperature-to-humidity",
             "humidity-to-location")
REVERSE_ORDER = tuple(reversed(MAP_ORDER))


def make_dict_seed(data):
    seed_row = data.split(":")
    seed_list = seed_row[1].split()
    seed_list = list(map(int, seed_list))
    seed_pairs = []
    sizes = []
    for i in range(len(seed_list) // 2):
        seed_pairs.append((seed_list[2*i], seed_list[2*i + 1]))
        sizes.append((seed_list[2*i], seed_list[2*i + 1]))
    seed_pairs.sort(key=lambda x: x[0])
    sizes.sort(key=lambda x: x[1])
    return seed_row[0].strip(), seed_pairs, sizes


def make_dict_map(data):
    map_row = data.split(":")
    map_list = map_row[1].split("\n")[1:]
    map_list = list(map(lambda x: x.split(), map_list))
    map_list = [[int(j) for j in i] for i in map_list]
    map_list.sort(key=lambda x: x[0])
    return map_row[0].strip()[:-4], map_list


def follow_map(start_val, map):
    for row in map:
        if start_val >= row[1] and start_val <= row[1] + row[2]:  # we have a hit
            offset = start_val - row[1]
            return row[0] + offset
    return start_val


def backtrack_map(end_val, map):
    for row in map:
        if end_val < row[0]:
            return end_val
        elif end_val >= row[0] and end_val < row[0] + row[2]:
            offset = end_val - row[0]
            return row[1] + offset
    return end_val


def do_full_backtrack(value, data):
    for map in REVERSE_ORDER:
        value = backtrack_map(value, data[map])
        # print(map.split("-")[0], value)
    return value


def test_seed(test, seeds):
    for set in seeds:
        if test >= set[0] and test < set[0] + set[1]:
            return True
    return False


def process_seed(seed, data):
    next_val = seed
    for map in MAP_ORDER:
        next_val = follow_map(next_val, data[map])
    return next_val


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if DEBUG:
        file = "example1.txt"
    else:
        file = "puzzle.txt"
    with open(file, "r") as f:
        data_string = f.read()
    data_list = data_string.split("\n\n")
    # print(data_list)
    data = {}
    name, seeds, sizes = make_dict_seed(data_list[0])
    # print(data)
    for row in data_list:
        # print(row)
        name, vals = make_dict_map(row)
        data[name] = vals
        # print(data)
    data.pop("s")
    print(seeds, data)
    step_size = sizes[0][1]
    test_loc = 0
    repeat = True
    while repeat:
        if step_size < 10:
            repeat = False
            step_size = 1
        candidate_seed = do_full_backtrack(test_loc, data)
        while not test_seed(candidate_seed, seeds):
            test_loc += step_size
            candidate_seed = do_full_backtrack(test_loc, data)
            # print(test_loc, candidate_seed)
        print(test_loc, candidate_seed, "coarse target",step_size)
        test_loc -= step_size
        step_size //= 100

    step_size /= 100
    while not test_seed(candidate_seed, seeds):
        test_loc += 1
        candidate_seed = do_full_backtrack(test_loc, data)
        # print(test_loc, candidate_seed)
    print("ANSWER +======++==+== ", test_loc + 1)
    # outputs = []
    # print(do_full_backtrack(86, data))
    # print(test_seed(do_full_backtrack(86, data), seeds))
    # for seed_set in seeds:
    #     start = seed_set[0]
    #     halfway = seed_set[1] // 2
    #     for i in range(seed_set[1]):
    #         outputs.append(process_seed(start+i, data))
    #         if i == halfway:
    #             print("Halfway!!")
    #     print(seed_set,"done")
    # # for next_val in seeds:
    # #     outputs.append(process_seed(next_val, data))
    # print("ANSWER +======++==+== ",min(outputs))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
