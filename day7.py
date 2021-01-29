from collections import defaultdict
from typing import List, Dict, NamedTuple
import re


TEST_RULES = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

class Bag(NamedTuple):
    # contains: color => count map
    color: str
    contains: List[str]


def parse_rule(rule:str):
    color = rule.split(" bags ")[0]
    #print("color:", color)
    
    contains = {}
    contains_part = rule.split( " contain ")[-1]
    for conts in contains_part.split(", "):
        #print("conts:", conts)
        if conts == "no other bags.":
            return Bag(color, {})

        num_bags = int(conts.split(" ")[0])
        first_space = conts.find(" ")
        contained_color = re.sub(' bags?', '', conts[first_space+1:].replace(".", ""))
        contains[contained_color] = num_bags
    
    return Bag(color, contains)


def make_bags(rules:str): 
    return [parse_rule(rule) for rule in rules.split("\n")]


def get_parents(bags):
    # given color, get list of immediate parent colors that can contain this
    parents = defaultdict(list)
   
    for bag in bags:
        for child_color in bag.contains:
            parents[child_color].append(bag.color)
    
    return parents


def can_eventually_contain(color:str, bags):
    parents = get_parents(bags)

    check = [color]
    can_contain = set()

    while check:
        curr_color = check.pop()
        for parent_color in parents[curr_color]:
            if not parent_color in can_contain:
                can_contain.add(parent_color)
                check.append(parent_color)

    return list(can_contain)


MY_BAG_COLOR = "shiny gold"
# Unit test
test_bags = make_bags(TEST_RULES)
assert len(can_eventually_contain(MY_BAG_COLOR, test_bags)) == 4


# read in the data
with open("./inputs/day7.txt") as f:
    rules = f.read()

# PART A:
bags = make_bags(rules)
print(len(can_eventually_contain(MY_BAG_COLOR, bags)))


# PART B:
# How many individual bags are required inside your single shiny gold bag
# start with own bag. Follow the path downstream and count the bags. Stack-based approach
# Data structure stack with color, multiplier
# Color, multiplier

def count_bags(color:str, bags:List) -> int:
    num_bags = 0  # How many individual bags  required inside your single shiny gold bag

    color_to_bag_map = {bag.color: bag for bag in bags}
    stack = [(color, 1)]  # color, multiplier
    # if we have one original bag, that contains 3 bags of type x, and then each x bag contains 2 y bags
    # --> eventually have in stack: (color x, 3)... (color y, 3*2 = 6)
    # So the multiplier keeps track of how many of these were there in total...
    # So no need to check each and everyone separately
 
    while stack:
        # pop
        bag_color, multiplier = stack.pop()
        bag = color_to_bag_map[bag_color]

        # account the childs
        for child_color, count in bag.contains.items():
            num_bags += multiplier * count
            stack.append((child_color, multiplier * count))

    return num_bags

assert count_bags(MY_BAG_COLOR, test_bags) == 32
print(count_bags(MY_BAG_COLOR, bags))


