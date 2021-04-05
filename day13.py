# https://adventofcode.com/2020/day/13
# About Chinese Remainder Theorem
from typing import List, Tuple

##############
# Solution
##############

def parse_input(raw_str:str) -> Tuple[int, List[int]]:
    s =  raw_str.split("\n")
    assert len(s) == 2

    earliest = int(s[0])
    ids = [None if el == "x" else int(el) for el in s[1].split(",")]

    return earliest, ids


def next_bus_and_time(ids, start_time=0):
    t = start_time
    ids_in_operation = [id_ for id_ in ids if id_ is not None]

    while True:
        for id_ in ids_in_operation:
            if t % id_ == 0:
                yield id_, t
        t += 1


# for part 2:
# Chinese remainder theorem
# if one knows the remainders of the Euclidean division of an integer n by several integers, then one can determine uniquely the remainder of the division of n by the product of these integers, under the condition that the divisors are pairwise coprime.
# https://en.wikipedia.org/wiki/Chinese_remainder_theorem#Search_by_sieving

# 7,13,x,x,59,x,31,19

# numbers that are congruent to 4 modulo 5 (will give remainder of 4 when divided by 5): 5,9,...
"""
t:   t % 7 == 0                                             t = 0 (mod 7)
t+1: t+1 % 13 == 0 --> t % 13 == 13 - 1     t = k*13 + 12   t = 12 (mod 13)
t+4: t+4 % 59 == 0 --> t % 59 == 59 - 4                     t = 56 (mod 59)
t+6: t+6 % 31 == 0 --> t % 31 == 31 - 6                     t = 25 (mod 31)
t+7: t+7 % 19 == 0 --> t % 19 == 19 - 7                     t = 12 (mod 19)
"""



def next_full_match(ids, start_time=0):
    """naive approach... exponential time algo, will never finish!"""
    oper_ids = [(idx, id_) for idx, id_ in enumerate(ids) if id_ is not None]

    base_cycle = oper_ids[0][1]
    t = start_time
    while True:
        if all((t + idx) % id_ == 0 for idx, id_ in oper_ids):
            yield t
        t += base_cycle


def first_full_match(ids):
    """Sieving approach to the chinese remainder theorem"""
    oper_ids = [(idx, id_) for idx, id_ in enumerate(ids) if id_ is not None]
    oper_ids = sorted(oper_ids, key=lambda x: x[1], reverse=True)
    rems = [(id_ - idx) % id_ if idx > 0 else 0 for idx, id_ in oper_ids]  # remainders

    add = oper_ids[0][1]
    #num = add - oper_ids[0][0]  # but adds the missing add in the loop
    num = - oper_ids[0][0]

    for (_, m), rem in zip(oper_ids[1:], rems[1:]):
        #print(f"m:{m}, rem:{rem}, add:{add}, num:{num}")
        while True:
            num += add
            if num % m == rem:
                add *= m
                break

    return num



##############
# Test cases
###############
RAW = """939
7,13,x,x,59,x,31,19"""

earliest, ids = parse_input(RAW)

# Part 1
bus_generator = next_bus_and_time(ids, earliest)
bus_id, departure_time = next(bus_generator)
assert bus_id * (departure_time - earliest) == 295

# Part 2:
full_match_generator = next_full_match(ids)
assert next(full_match_generator) == 1068781
assert first_full_match(ids) == 1068781


RAW3 = """0
67,7,x,59,61"""

earliest3, ids3 = parse_input(RAW3)
assert first_full_match(ids3) == 1261476


RAW4 = """0
1789,37,47,1889"""

earliest4, ids4 = parse_input(RAW4)
assert first_full_match(ids4) == 1202161486


##############
# Driver
##############

with open("./inputs/day13.txt") as f:
    earliest, ids = parse_input(f.read())

# Part 1
bus_generator = next_bus_and_time(ids, earliest)
bus_id, departure_time = next(bus_generator)
print("Part 1:", bus_id * (departure_time - earliest))

# Part 2
print("Part 2:", first_full_match(ids))
