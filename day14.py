# https://adventofcode.com/2020/day/14

from collections import defaultdict
from typing import List, Dict
from itertools import product

##############
# Solution
##############


def to_binary_old(val: int, num_bits=36) -> str:
    bits = []
    for _ in range(num_bits):
        bits.append(val % 2)
        val = val // 2

    return bits[::-1]


def to_binary(val: int, num_bits=36) -> List[str]:
    return list("{0:036b}".format(val))

assert to_binary(65) == [i for i in "000000000000000000000000000001000001"]


# Part 1:
def apply_mask(val: int, mask:str) -> str:
    val_bits = to_binary(val)
    assert len(val_bits) == len(mask)

    for idx, mask_bit in enumerate(mask):
        if mask_bit == "1":
            val_bits[idx] = "1"
        elif mask_bit == "0":
            val_bits[idx] = "0"

    return int("".join(val_bits), 2) 


# Part 2:
def get_mem_locs(mem_pos: int, mask: str) -> int:
    """For part 2, yields all mem locations where the value must be set.
    Floating bits lead to cartesian product of mem locations:
    The value must be set to all possible combinations
    """

    orig_loc_bits = to_binary(mem_pos)
    assert len(orig_loc_bits) == len(mask)

    floating_idx = []  # get the floating bit indices
    for idx, mask_bit in enumerate(mask):
        if mask_bit == "1":
            orig_loc_bits[idx] = "1"
        if mask_bit == "X":
            floating_idx.append(idx)

    floating_selection = [["0", "1"] for _ in floating_idx]

    # case with no floating bits
    if len(floating_idx) == 0:
        yield int("".join(orig_loc_bits), 2)

    for bit_combination in product(*floating_selection):
        new_bits = orig_loc_bits.copy()
        for i, bit in zip(floating_idx, bit_combination):
            new_bits[i] = bit

        yield int("".join(new_bits), 2) 


def run(prog: List[str], mem_addr_decoder_mode=False) -> Dict[int, int]:
    mem = defaultdict(int)
    mask = "X" * 36

    for cmd in prog:
        if cmd.startswith("mask = "):
            mask = cmd.split(" = ")[-1]
        elif cmd.startswith("mem["):
            mem_s, val_s = cmd.split(" = ")
            val = int(val_s)
            pos = int(mem_s[4:-1])

            if not mem_addr_decoder_mode:  # Part 1
                mem[pos] = apply_mask(val, mask)
            else:  # Part 2:
                # Cartesian product of the mem locations
                # Generator to give them one by one
                for mpos in get_mem_locs(pos, mask):
                    mem[mpos] = val
        else:
            raise RuntimeError(f"Unknown command {cmd}")

    return mem


##############
# Test cases
###############
RAW = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

TEST_PROG = RAW.split("\n")
test_mem = run(TEST_PROG)
assert sum(test_mem.values()) == 165

# For part 2
RAW2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""

TEST_PROG2 = RAW2.split("\n")
test_mem2 = run(TEST_PROG2, mem_addr_decoder_mode=True)
assert sum(test_mem2.values()) == 208


##############
# Driver
##############
with open("./inputs/day14.txt") as f:
    prog = [line.strip() for line in f]

# Part 1
mem = run(prog)
print("Part 1:", sum(mem.values()))

# Part 2
mem2 = run(prog, mem_addr_decoder_mode=True)
print("Part 2:", sum(mem2.values()))
