from typing import NamedTuple

TEST_OP_LINES = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""


# list of ops
class Op(NamedTuple):
    type: str
    arg: int


def parse_line(line:str) -> Op:
    parts = line.strip().split()
    return Op(parts[0], int(parts[1]))


def make_ops(lines):
    return [parse_line(line) for line in lines.split("\n")]


def run_until_loop_starts(ops):
    # returns the acc value before enters a loop
    ops_seen = set()
    op_nbr = 0
    acc = 0

    while op_nbr not in ops_seen:
        ops_seen.add(op_nbr)
        op = ops[op_nbr]

        if op.type == "nop":
            op_nbr += 1
        elif op.type == "acc":
            acc += op.arg
            op_nbr += 1
        elif op.type == "jmp":
            op_nbr += op.arg

    return acc

test_ops = make_ops(TEST_OP_LINES)
assert run_until_loop_starts(test_ops) == 5


with open("./inputs/day8.txt") as f:
    ops = make_ops(f.read())

print(run_until_loop_starts(ops))


# part B:
def test_prog(ops, op_nbr, ops_seen, acc):
    # returns True, acc-val if the prog runs until it tries to access the row just out of bounds from the end
    # else returns False, 0
    ops_seen = ops_seen.copy()

    while op_nbr not in ops_seen:
        ops_seen.add(op_nbr)
        op = ops[op_nbr]

        if op.type == "nop":
            op_nbr += 1
        elif op.type == "acc":
            acc += op.arg
            op_nbr += 1
        elif op.type == "jmp":
            op_nbr += op.arg

        if op_nbr == len(ops):
            # found the sol:
            return True, acc
        if op_nbr < 0 or op_nbr > len(ops):
            return False, 0
        
    return False, 0


def fix_code(ops):
    # swap first possible, try what happens...
    # then swap the next possibility... next
    ops_seen = set()
    op_nbr = 0
    acc = 0

    while op_nbr not in ops_seen:
        op = ops[op_nbr]

        if op.type == "acc":
            ops_seen.add(op_nbr)
            acc += op.arg
            op_nbr += 1
        elif op.type == "nop":
            old_op = op
            ops[op_nbr] = Op("jmp", op.arg)
            valid, rst = test_prog(ops, op_nbr, ops_seen, acc)
            if valid:
                return rst
            # revert back
            ops[op_nbr] = old_op
            ops_seen.add(op_nbr)
            # normal step
            op_nbr += 1
        elif op.type == "jmp":
            old_op = op
            ops[op_nbr] = Op("nop", op.arg)
            valid, rst = test_prog(ops, op_nbr, ops_seen, acc)
            if valid:
                return rst
            # revert back
            ops[op_nbr] = old_op
            ops_seen.add(op_nbr)
            # normal step
            op_nbr += op.arg


assert fix_code(test_ops) == 8

print(fix_code(ops))
