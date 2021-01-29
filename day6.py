from collections import Counter

TEST_DATA = """abc

a
b
c

ab
ac

a
a
a
a

b"""



def count_yeses(answers:str) -> int:
    # anyone answered yes in the group
    groups = answers.split("\n\n")
    
    return sum(len(set(group.replace("\n", ""))) for group in groups)

assert count_yeses(TEST_DATA) == 11


def count_yeses2(answers:str) -> int:
    # EVERYONE answered yes in the group
    groups = answers.split("\n\n")
    num_yeses = 0

    for group in groups:
        group_size = len(group.split("\n"))
        num_yeses += sum(count == group_size for count in Counter(group.replace("\n", "")).values())

    return num_yeses

assert count_yeses2(TEST_DATA) == 6

# problem input
with open("./inputs/day6.txt") as f:
    answers = f.read()
print("Part A:", count_yeses(answers))
print("Part B:", count_yeses2(answers))