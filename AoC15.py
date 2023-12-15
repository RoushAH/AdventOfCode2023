import time
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import pprint

import functools as ft
import difflib

DEBUG = False
EQ = "="
DASH = "-"
boxes = [[] for i in range(256)]


@ft.cache
def process_string2(chars):
    score = 0
    for char in chars:
        score += ord(char)
        score *= 17
        score %= 256
    return score


@ft.cache
def process_string(chars):
    if EQ in chars:
        charlist = chars.split(EQ)
        charlist[1] = int(charlist[1])
    else:
        charlist = [chars[:-1], None]
    charlist.append(process_string2(charlist[0]))
    # print(charlist)
    return charlist


def do_lens_job(new_lens):
    global boxes
    box = boxes[new_lens[2]]
    label = new_lens[0]
    job = new_lens[1]
    if job is None: # REMOVE
        # print(job, new_lens)
        box = list(filter(lambda x: x[0] != label, box))
        # print(f"box{new_lens[2]} = {box}")
        # input()
    else: # insert/replace
        hits = [x[0] != label for x in box]
        if all(hits):
            box.append(new_lens)
        else:
            spot = hits.index(False)
            box[spot] = new_lens
    # print(new_lens[2],box)
    boxes[new_lens[2]] = box
    # time.sleep(.5)


if __name__ == '__main__':
    if DEBUG:
        file = "data/example2.txt"
    else:
        file = "data/puzzle2.txt"
    with open(file, "r") as f:
        data_string = f.read()
    data_string = data_string.split(",")
    print(data_string)
    answer = 0
    data_list_processed = []
    # print(boxes)
    with Pool() as pool:
        results = pool.imap(process_string, data_string)
        for result in results:
            print(result)
            do_lens_job(result)
            data_list_processed.append(result)
    # for elem in data_string:
    #     answer += process_string(elem)
    # print(answer)
    # print(data_list_processed)
    # for elem in results:
    #     print(elem)
    for box_num, box in enumerate(boxes,1):
        for slot_num, lens in enumerate(box,1):
            score = box_num * slot_num * lens[1]
            print(box_num, score, box)
            answer += score
    print(answer)