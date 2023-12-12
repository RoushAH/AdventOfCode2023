DEBUG = False
GALAXY = "#"
galaxies = []
galaxy_x = []
galaxy_y = []
empty_x = []
empty_y = []
EXPANSION = 1000000


def collapse(array):
    taxicab = 0
    for i, start in enumerate(array[:-1]):
        for finish in array[i+1:]:
            taxicab += abs(finish - start)
    return taxicab


def expand_direction(array, empties, expansion = 1):
    output = []
    for element in array:
        offset = element + (expansion-1) * sum(i < element for i in empties)
        output.append(offset)
    return output


def find_empties(array, empties, max):
    for val in range(max):
        if val not in array:
            empties.append(val)


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches


def find_galaxies(array):
    for y, row in enumerate(array):
        found = list(find_all(row, GALAXY))
        for x in found:
            galaxies.append((y,x))


if __name__ == '__main__':
    if DEBUG:
        file = "data/example1.txt"
    else:
        file = "data/puzzle.txt"
    with open(file, "r") as f:
        data_string = f.read()
    data_string = data_string.split("\n")
    # print(data_string)
    find_galaxies(data_string)
    print(galaxies)
    galaxy_y, galaxy_x = list(zip(*galaxies))
    find_empties(galaxy_x, empty_x, len(data_string[0]))
    find_empties(galaxy_y, empty_y, len(data_string))
    galaxy_y = expand_direction(galaxy_y, empty_y, EXPANSION)
    galaxy_x = expand_direction(galaxy_x, empty_x, EXPANSION)
    print(galaxy_x)
    print(collapse(galaxy_x) + collapse(galaxy_y))