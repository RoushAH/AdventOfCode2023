from functools import reduce
DEBUG = False
MOVE = {"R":1, "L":0}
nodes = {}
primes = []


def make_move(node, move):
       return nodes[node][MOVE[move]]


def list_primes(max):
    candidate = 2
    while candidate <= max:
        is_prime = True
        for prime in primes:
            if candidate % prime == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1


def prime_factors(num):
    factors = []
    for prime in primes:
        while num % prime == 0:
            factors.append(prime)
            num /= prime
    return factors


def LCM(items):
    factors = list(map(prime_factors, items))
    print(factors)
    answer = 307
    for item in factors:
        answer *= item[0]
    return answer


def LCM_honest(items):
    factors = list(map(prime_factors, items))
    answer = factors[0]
    factors = factors[1:]
    while len(factors) > 0:
        for factor in factors:
            for item in factor:
                if item in answer:
                    factor.remove(item)
            answer += factor
            factors = factors[1:]
    answer = reduce(lambda x,y: x*y, answer)
    return answer


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if DEBUG:
        file = "data/example2.txt"
    else:
        file = "data/puzzle.txt"
    with open(file, "r") as f:
        data_string = f.read()
    # print(data_string)
    data_list = data_string.split("\n")
    instructions = list(data_list[0])
    # print(instructions)
    for row in data_list[2:]:
        name = row[:row.find("=")].strip()
        left = row[7:10]
        right = row[12:-1]
        nodes[name] = (left, right)
    current_nodes = [name for name in nodes if name.endswith("A")]
    time_of_flight = [0 for _ in current_nodes]
    final_nodes = ["" for _ in current_nodes]
    # node = "AAA"
    # while node != "ZZZ":
    #     instruction = instructions[step % len(instructions)]
    #     node = make_move(node, instruction)
    #     step += 1
    for pos, this_node in enumerate(current_nodes):
        step = 0
        while not this_node.endswith("Z"):
            instruction = instructions[step % len(instructions)]
            this_node = make_move(this_node, instruction)
            step += 1
        time_of_flight[pos] = step
        final_nodes[pos] = this_node
    print(current_nodes, time_of_flight, final_nodes)
    list_primes(max(time_of_flight))
    print(LCM(time_of_flight))
    print(LCM_honest(time_of_flight))
