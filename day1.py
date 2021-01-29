from typing import List

TEST_INPUT = [1721,
                979,
                366,
                299,
                675,
                1456]



def find_product(numbers: List[int], adds_to=2020) -> int:
    needs = {adds_to - num for num in numbers}
    for num in numbers:
        if num in needs:
            return num * (adds_to - num)

assert find_product(TEST_INPUT) == 514579


with open("./inputs/day1.txt") as f:
    numbers = [int(line.strip()) for line in f]

print("Part A:", find_product(numbers))


# Part B:
def find_product_sum_of_three(numbers: List[int], adds_to=2020) -> int:
    needs = {adds_to - i - j: (i, j) 
                for idx_i, i in enumerate(numbers)
                for idx_j, j in enumerate(numbers)
                if idx_i != idx_j}

    for num in numbers:
        if num in needs:
            i, j = needs[num]
            return num * i * j

assert find_product_sum_of_three(TEST_INPUT) == 241861950

print("Part A:", find_product_sum_of_three(numbers))