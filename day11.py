from collections import Counter

ADJS = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0)
]

EMPTY = "L"
FLOOR = "."
OCCUPIED = "#"

# floor (.), an empty seat (L), or an occupied seat (#)


# Rules
# (one of the eight positions immediately up, down, left, right, or diagonal from the seat)

# If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
# If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
# Otherwise, the seat's state does not change.

# Floor (.) never changes; seats don't move, and nobody sits on the floor.


def get_adjs_counts(grid, pos):
    row, col = pos
    rows = len(grid)
    cols = len(grid[0])

    return Counter([grid[row + dr][col + dc]
                        for dr, dc in ADJS
                        if 0 <= row + dr < rows and  0 <= col + dc < cols])


def get_visible_counts(grid, pos):
    row, col = pos
    rows = len(grid)
    cols = len(grid[0])
    chairs = []

    for dr, dc in ADJS:
        #dr, dc define a direction
        steps = 1
        while True:
            if not (0 <= row + dr*steps < rows) or \
               not (0 <= col + dc*steps < cols):
               break 

            if grid[row + dr*steps][col + dc*steps] in (EMPTY, OCCUPIED):
                chairs.append(grid[row + dr*steps][col + dc*steps])
                break

            steps += 1

    return Counter(chairs)


def next_state(grid, pos, method="adjs"):
    row, col = pos
    if grid[row][col] == FLOOR:
        # floor never changes
        return FLOOR

    if method == "adjs":
        adj_counts = get_adjs_counts(grid, pos)
        if grid[row][col] == OCCUPIED and adj_counts["#"] >= 4:
            return EMPTY
    #print(adj_counts)
    if method == "visible":
        adj_counts = get_visible_counts(grid, pos)
        if grid[row][col] == OCCUPIED and adj_counts["#"] >= 5:
            return EMPTY
    
    if grid[row][col] == EMPTY and adj_counts["#"] == 0:
        return OCCUPIED
    #if grid[row][col] == OCCUPIED and adj_counts["#"] >= 4:
    #    return EMPTY

    return grid[row][col]


def step(grid, method="adjs"):
    #new_grid = grid.deepcopy()  # would need to make a deepcopy to copy also the inner lists
    new_grid = [[None]*len(grid[0]) for _ in range(len(grid))]

    rows = len(grid)
    cols = len(grid[0])

    for row in range(rows):
        for col in range(cols):
            new_grid[row][col] = next_state(grid, (row, col), method=method)
            #print(f"@{row}{col}: {new_grid[row][col]} ( old: {grid[row][col]})")

    return new_grid


def count_occupied(grid):
    return sum(el == OCCUPIED for row in grid for el in row)


def step_until_stable(grid, method="adjs"):
    curr_grid = grid
    while True:
        new_grid = step(curr_grid, method)

        if new_grid == curr_grid:
            return new_grid

        curr_grid = new_grid


###
# TEST CASES
###
RAW_GRID_TEST = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""


grid_test = [[el for el in row.strip()] for row in RAW_GRID_TEST.split("\n")]

# Part A
assert count_occupied(step_until_stable(grid_test)) == 37

# Part B
assert count_occupied(step_until_stable(grid_test, method="visible")) == 26


###
# Problem
###

with open("./inputs/day11.txt") as f:
    grid = [[el for el in row.strip()] for row in f.read().split("\n")]

# Part A:
print("Part A:", count_occupied(step_until_stable(grid, method="adjs")))


# Part B:
print("Part B:", count_occupied(step_until_stable(grid, method="visible")))