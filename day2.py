import re
from typing import List

RE_POLICY_PASSWORD = r"^(\d+)-(\d+) (\w): (.*)"

TEST_POLICIES = ["1-3 a: abcde",
                "1-3 b: cdefg",
                "2-9 c: ccccccccc"]


def split_policy_line(policy_and_pwd):
    match = re.match(RE_POLICY_PASSWORD, policy_and_pwd)
    if match:
        min_repeats = int(match.group(1))
        max_repeats = int(match.group(2))
        char = match.group(3)
        pwd = match.group(4)
    else:
        raise ValueError("Policy-password string wrong kind")
    return min_repeats, max_repeats, char, pwd


def is_pwd_valid(policy_and_pwd: str) -> bool:
    min_repeats, max_repeats, char, pwd = split_policy_line(policy_and_pwd)
    count = pwd.count(char)
    if count > max_repeats or count < min_repeats:
        return False
    else:
        return True


def get_number_of_valid_passwords(password_list: List[str]) -> int:
    num_valids = 0
    for line in password_list:
        if is_pwd_valid(line):
            num_valids += 1
    return num_valids

assert get_number_of_valid_passwords(TEST_POLICIES) == 2

# Part 1:
with open("./inputs/day2.txt") as f:
    password_list = [line.strip() for line in f]

print("Part 1:", get_number_of_valid_passwords(password_list))

# Part 2:
def is_pwd_valid2(policy_and_pwd: str) -> bool:
    idx1, idx2, char, pwd = split_policy_line(policy_and_pwd)

    hits = 0
    if idx1 <= len(pwd):
        if pwd[idx1-1] == char: hits += 1
    if idx2 <= len(pwd):
        if pwd[idx2-1] == char: hits += 1

    return True if hits == 1 else False

def get_number_of_valid_passwords2(password_list: List[str]) -> int:
    num_valids = 0
    for line in password_list:
        if is_pwd_valid2(line):
            num_valids += 1
    return num_valids

assert get_number_of_valid_passwords2(TEST_POLICIES) == 1

print("Part 2:", get_number_of_valid_passwords2(password_list))
