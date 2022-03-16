# https://adventofcode.com/2020/day/15

from typing import List, Iterator

##############
# Solution
##############

def get_next_number(starting_numbers: List[int]) -> Iterator[int]:
    """
    """
    last_seen = {}  # nbr as a key, val is the turn it was last seen
    turn = 0

    prev_nbr = None  # for the first
    for nbr in starting_numbers:
        if prev_nbr is not None:
            last_seen[prev_nbr] = turn  # refers still to the previous turn
        turn += 1
        prev_nbr = nbr
        yield nbr

    # then loop indefinitely and yield numbers one by one
    while True:       
        if prev_nbr not in last_seen:
            # say zero
            nbr = 0
        else:
            # say age since last occurence 
            nbr = turn - last_seen[prev_nbr]

        last_seen[prev_nbr] = turn  # update prev_nbr
        turn += 1  
        prev_nbr = nbr
        yield nbr


##############
# Test cases
###############

STARTING_NBRS_TEST = [0,3,6]

test_nbrs = get_next_number(STARTING_NBRS_TEST)
for _ in range(2020):
    test_2020th = next(test_nbrs)
assert test_2020th == 436


# Given the starting numbers 3,1,2, the 2020th number spoken is 1836.
test_nbrs = get_next_number([2,3,1])
for _ in range(2020):
    test_2020th = next(test_nbrs)
assert test_2020th == 78

# Given the starting numbers 3,1,2, the 2020th number spoken is 1836.
test_nbrs = get_next_number([3,1,2])
for _ in range(2020):
    test_2020th = next(test_nbrs)
assert test_2020th == 1836

##############
# Driver
##############

starting_nbrs = [17,1,3,16,19,0]
nbrs = get_next_number(starting_nbrs)

# Part 1
for _ in range(2020):
    nbr_2020th = next(nbrs)

print("Part 1:", nbr_2020th)


# Part 2
# Not too slow...
nbrs = get_next_number(starting_nbrs)
for i, _ in enumerate(range(30000000)):
    if i % 10_000 == 0:
        print(i, i / 30000000)
    nbr_30000000th = next(nbrs)

print("Part 2:", nbr_30000000th)
