DEBUG = False


def string_into_int(string):
    if string == "":
        return ""
    string = string[string.index(":")+1:].strip()
    string = string.replace(" ","")
    return int(string)


def calc_dist(press, time):
    time -= press
    speed = press
    distance = speed * time
    return distance


def attempt_race(race):
    time = race[0]
    record_distance = race[1]
    candidate_distance = 0
    press = 0
    step_size = 1000000
    repeat = True
    while repeat:
        print(step_size)
        if step_size < 10:
            step_size = 1
            repeat = False
        while candidate_distance <= record_distance:
            candidate_distance = calc_dist(press, time)AoC6.py
            press += step_size
        print(candidate_distance, step_size)
        press -= step_size
        step_size //= 100
    return press, time-press


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if DEBUG:
        file = "data/example1.txt"
    else:
        file = "data/puzzle.txt"
    with open(file, "r") as f:
        data_string = f.read()
    print(data_string)
    data_list = data_string.split("\n")

    print(data_list)
    data_list = list(map(string_into_int, data_list))
    # for race in data_list:
    race = data_list
    race_result = attempt_race(race)
    score = (race_result[1] - race_result[0] + 1)
    print(race, race_result, score)
    print("ANSWER = ",score)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
