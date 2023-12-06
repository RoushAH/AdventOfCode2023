DEBUG = False


def split_ticket(ticket):
    ticket = ticket.split("|")
    winners = list(map(int, ticket[0].split()))
    numbers = list(map(int, ticket[1].split()))
    return {"winners":winners, "numbers":numbers}


def get_score(ticket):
    score = 0
    for num in ticket["numbers"]:
        if num in ticket["winners"]:
            score += 1
    return score


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file = "puzzle.txt"
    if DEBUG:
        file = "example1.txt"
    with open(file, "r") as f:
        data_string = f.read()
    data = data_string.split("\n")
    data = list(map(lambda x: x.split(":")[1].strip(), data))
    cards = list(map(split_ticket, data))
    count_cards = [1 for card in cards]
    for pos, card in enumerate(cards):
        score = get_score(card)
        for i in range (score):
            count_cards[i+pos+1] += count_cards[pos]
    print(sum(count_cards))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
