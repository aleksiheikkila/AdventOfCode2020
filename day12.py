
from dataclasses import dataclass
from typing import NamedTuple


class Action(NamedTuple):
    type: str
    amt: int

    @staticmethod
    def parse(line:str):
        return Action(type=line[0], amt=int(line[1:]))


@dataclass
class Ship:
    x: int = 0
    y: int = 0
    dir: int = 0  # unit circle kind of an angle. East = 0, N = 90 etc.

    def move(self, action: Action):
        if action.type == "N":
            self.y += action.amt
        elif action.type == "S":
            self.y -= action.amt
        elif action.type == "E":
            self.x += action.amt
        elif action.type == "W":
            self.x -= action.amt
        elif action.type == "L":
            self.dir = (self.dir + action.amt) % 360
        elif action.type == "R":
            self.dir = (self.dir - action.amt) % 360
        elif action.type == "F":
            if self.dir == 0:
                self.x += action.amt
            elif self.dir == 180:
                self.x -= action.amt
            elif self.dir == 90:
                self.y += action.amt
            elif self.dir == 270:
                self.y -= action.amt
            else:
                raise RuntimeError(f"Unknown direction: {dir}")
        else:
            raise RuntimeError(f"Unknown action: {action}")


# For part 2:
@dataclass
class ShipWithWaypoint:
    x: int = 0
    y: int = 0
    dir: int = 0  # unit circle kind of an angle. East = 0, N = 90 etc.

    wp_x: int = 10
    wp_y: int = 1
    # The waypoint is relative to the ship; that is, if the ship moves, the waypoint moves with it.

    def move(self, action: Action):
        if action.type == "N":
            self.wp_y += action.amt
        elif action.type == "S":
            self.wp_y -= action.amt
        elif action.type == "E":
            self.wp_x += action.amt
        elif action.type == "W":
            self.wp_x -= action.amt
        elif action.type == "L":
            for _ in range(action.amt // 90):  # how many turns
                self.wp_x, self.wp_y = -self.wp_y, self.wp_x
        elif action.type == "R":
            for _ in range(action.amt // 90):
                self.wp_x, self.wp_y = self.wp_y, -self.wp_x
        elif action.type == "F":
            # to the waypoint amt number of times
            self.x += (self.wp_x * action.amt)
            self.y += (self.wp_y * action.amt)
        else:
            raise RuntimeError(f"Unknown action: {action}")


####
# Unit tests
####

RAW = """F10
N3
F7
R90
F11"""

TEST_INSTRUCTIONS = [Action.parse(line) for line in RAW.split("\n")]

# Part 1
TEST_SHIP = Ship()
for instruction in TEST_INSTRUCTIONS:
    TEST_SHIP.move(instruction)

assert abs(TEST_SHIP.x) + abs(TEST_SHIP.y) == 25

# Part 2
TEST_SHIP2 = ShipWithWaypoint()
for instruction in TEST_INSTRUCTIONS:
    TEST_SHIP2.move(instruction)

assert abs(TEST_SHIP2.x) + abs(TEST_SHIP2.y) == 286


####
# Actual problem
####

# Part 1
with open("./inputs/day12.txt") as f:
    instructions = [Action.parse(line) for line in f.readlines()]

ship = Ship()
for instr in instructions:
    ship.move(instr)

print(ship)
print("Manhattan dist:", abs(ship.x) + abs(ship.y))


# Part 2:
ship2 = ShipWithWaypoint()
for instr in instructions:
    ship2.move(instr)

print(ship2)
print("Manhattan dist:", abs(ship2.x) + abs(ship2.y))
