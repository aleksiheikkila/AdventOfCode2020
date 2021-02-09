
from typing import List
from collections import Counter

def get_differences(adapters: List[int]) -> List[int]:
    adapters = sorted(adapters.copy() + [0])  # adding the outlet with zero joltage
    # add also the device joltage:
    adapters.append(adapters[-1] + 3) 

    diffs = [rating2 - rating1 
            for rating1, rating2 in zip(adapters, adapters[1:])]

    assert all(diff in (1,2,3) for diff in diffs)  # must use all...

    return diffs


def diff_score(adapters: List[int]) -> int:
    diffs = get_differences(adapters)
    counts = Counter(diffs)

    return counts[1] * counts[3]


def possible_ways(adapters: List[int]) -> int:
    adapters = sorted(adapters.copy() + [0])
    adapters.append(adapters[-1] + 3) 
    device_joltage = adapters[-1]

    # costruct step by step.
    # how many ways to reach joltage x?
    # Its the sum of the number ways to reach x-1, x-2, x-3

    # array[n] for "how many ways to joltage n"
    num_ways = [0] * (device_joltage + 1)

    # first joltages (starting conditions):
    num_ways[0] = 1
    if 1 in adapters:  # the adapters are distinct (diffs are 1, 2, or 3)
        num_ways[1] = 1
    if 2 in adapters and 1 in adapters:
        num_ways[2] = 2
    elif 2 in adapters:
        # but not 1
        num_ways[2] = 1

    for joltage in range(3, device_joltage + 1):
        if joltage in adapters:
            num_ways[joltage] = num_ways[joltage - 3] + num_ways[joltage - 2] + num_ways[joltage - 1]

    return num_ways[device_joltage]


#
# Tests
# 

TEST_DATA1 = """16
10
15
5
1
11
7
19
6
12
4"""

TEST_DATA2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""


test_adapters_1 = [int(line.strip()) for line in TEST_DATA1.split("\n")]
test_adapters_2 = [int(line.strip()) for line in TEST_DATA2.split("\n")]

assert diff_score(test_adapters_1) == 5*7
assert diff_score(test_adapters_2) == 22*10


print("possible ways 1:", possible_ways(test_adapters_1))
assert possible_ways(test_adapters_1) == 8

print("possible ways 2:", possible_ways(test_adapters_2))
assert possible_ways(test_adapters_2) == 19208

#
# Problem
#

# Part A: 
# What is the number of 1-jolt differences multiplied by the number of 3-jolt differences?
with open("./inputs/day10.txt") as f:
    adapters = [int(line.strip()) for line in f.readlines()]

print("Part A, score:", diff_score(adapters))

# Part B:
# What is the total number of distinct ways you can arrange the adapters to connect 
# the charging outlet to your device?
print("Part B:", possible_ways(adapters))
