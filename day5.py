from typing import NamedTuple

class Seat(NamedTuple):
    row: int
    col: int

    @property
    def seat_id(self) -> int:
        return self.row * 8 + self.col

TEST_CASES = ["BFFFBBFRRR",
            "FFFBBBFRRR",
            "BBFFBBFRLL"]

def find_seat(boarding_pass) -> Seat:
    # Form a binary string, convert it to int
    row = int("".join([{"F": "0", "B": "1"}[c] for c in boarding_pass.strip()[:7]]), 2)
    col = int("".join([{"L": "0", "R": "1"}[c] for c in boarding_pass.strip()[7:10]]), 2)

    return Seat(row, col)

s = find_seat(TEST_CASES[0])
assert s.row == 70 and s.col == 7 and s.seat_id == 567
s = find_seat(TEST_CASES[1])
assert s.row == 14 and s.col == 7 and s.seat_id == 119
s = find_seat(TEST_CASES[2])
assert s.row == 102 and s.col == 4 and s.seat_id == 820

# Part A
with open("inputs/day05.txt") as f:
    seats = [find_seat(line.strip()) for line in f]

# What is the highest seat ID on a boarding pass?
print("Part A:", max((seat.seat_id for seat in seats)))  # 970


# Part B
# Need to find a gap between lowest and highest seat_id

seat_ids = [seat.seat_id for seat in seats]
lo = min(seat_ids)
hi = max(seat_ids)

print("Part B:", [seat_id for seat_id in range(lo, hi+1) 
                    if seat_id not in seat_ids and seat_id - 1 in seat_ids and seat_id + 1 in seat_ids])
# the plus minus conditions are not necessary
