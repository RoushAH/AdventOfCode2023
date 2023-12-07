DEBUG = False
HANDS = {
    "Five":7,
    "Four":6,
    "Full":5,
    "Three":4,
    "Two":3,
    "One":2,
    "High":1
}
VALS = ("A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J")
VALUES = {card:13-value for value, card in enumerate(VALS)}
print(VALUES)
joker_hands = []
# 249609189 was too low


def rank_hands(one, two):
    if one[2] == two[2]:
        for i in range(5):
            if VALUES[one[0][i]] > VALUES[two[0][i]]:
                return 1
            elif VALUES[two[0][i]] > VALUES[one[0][i]]:
                return -1
    if HANDS[one[2]] > HANDS[two[2]]:
        return 1
    else:
        return -1


def qsort_hand(hands):
    if len(hands) <= 1:
        return hands
    pivot = hands[0]
    lower = []
    higher = []
    for hand in hands[1:]:
        if rank_hands(pivot, hand) < 0:
            higher.append(hand)
        else:
            lower.append(hand)
    higher = qsort_hand(higher)
    lower = qsort_hand(lower)
    return lower+[pivot]+higher


def resolve_joker(hand, dupes):
    dupes.remove("J")
    if len(dupes) == 0:
        return "Five"
    new_hand = [i for i in hand if i != "J"]
    Js= hand.count("J")
    best = "High"
    best_hand = []
    for choice in dupes:
        test_hand = new_hand + [choice for j in range(Js)]
        type = determine_type(test_hand)
        # print(test_hand, type)
        if HANDS[type] > HANDS[best]:
            best = type
            best_hand = test_hand
    joker_hands.append(("".join(hand), best, "".join(best_hand)))
    # print(" winner ", best)
    return best


def determine_type(hand):
    hand = list(hand)
    dupes = set([x for x in hand])
    if "J" in hand:
        return resolve_joker(hand, dupes)
    if len(dupes) == 1:
        return "Five"
    elif len(dupes) == 5:
        return "High"
    elif len(dupes) == 4:
        return "One"
    elif len(dupes) == 3: # Three distinct could be two pair or three of a kind
        hits = [0, 0, 0]
        for i, card in enumerate(dupes):
            hits[i] = hand.count(card)
        hits.sort(reverse=True)
        if hits[0] == 3:
            return "Three"
        return "Two"
    elif len(dupes) == 2: # Two distinct could be full house or 4 of a kind
        hits = [0, 0]
        for i, card in enumerate(dupes):
            hits[i] = hand.count(card)
        hits.sort(reverse=True)
        if hits[0] == 4:
            return "Four"
        return "Full"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if DEBUG:
        file = "data/example1.txt"
    else:
        file = "data/puzzle.txt"
    with open(file, "r") as f:
        data_string = f.read()
    # print(data_string)
    data_list = data_string.split("\n")
    data_list = list(map(lambda x: x.split()+[0 , 0], data_list))
    # stored with an int "score" after each
    # print(data_list)
    for hand in data_list:
        hand[2] = determine_type(hand[0])
    for jhand in joker_hands:
        if jhand[0].count("J") > 1:
            print( jhand )
    sorted = qsort_hand(data_list)
    sum = 0
    for pos, hand in enumerate(sorted, 1):
        sum += pos * int(hand[1])
        print(pos, hand)
    print(sum)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
