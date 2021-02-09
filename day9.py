# https://adventofcode.com/2020/day/9
# Brute force approach as the input is small-ish

from collections import deque

def not_sums(numbers, window_len=25):
    window = deque(maxlen=window_len)

    for i, num in enumerate(numbers):
        if i < window_len:
            # preamble not considered
            window.append(num)
        else:
            sums = {n1 + n2
                    for i, n1 in enumerate(window) 
                    for j, n2 in enumerate(window)
                    if i > j}
            if num not in sums:
                yield num
            window.append(num)


def get_contiguous_slice(numbers, target):
    # brute force
    for i, num in enumerate(numbers):
        s = num
        for j in range(i+1, len(numbers)):
            s += numbers[j]
            if s == target:
                return numbers[i:j+1]
            if s > target:
                break

def get_weakness(numbers, target):
    num_slice = get_contiguous_slice(numbers, target)
    return min(num_slice) + max(num_slice)

#
# Test cases
# 

TESTDATA = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

test_numbers = [int(num) for num in TESTDATA.split("\n")]

# Part a
assert next(not_sums(test_numbers, 5)) == 127
# Part b:
assert get_weakness(test_numbers, 127) == 62


#
# Problem
#

with open("./inputs/day9.txt") as f:
    numbers = [int(line) for line in f.read().split("\n")]

# Part A
first_invalid = next(not_sums(numbers))
print("Part A:", first_invalid)

# Part B
print("Part B:", get_weakness(numbers, first_invalid))
