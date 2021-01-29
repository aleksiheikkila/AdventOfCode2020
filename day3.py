
TEST_MAP = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#""".split("\n")


def trees_encountered(terrain_map, stepsize_right=3, stepsize_down=1):
    num_rows, num_cols = len(terrain_map), len(terrain_map[0])
    trees_encountered = 0

    for stepno, rowno in enumerate(range(0, num_rows, stepsize_down)):
        if terrain_map[rowno][(stepsize_right * stepno) % num_cols] == "#":
            trees_encountered += 1

    return trees_encountered

assert trees_encountered(TEST_MAP) == 7
assert trees_encountered(TEST_MAP, 3, 1) == 7


with open("./inputs/day3.txt") as f:
    terrain = [line.strip() for line in f]

# Part A:
print("Part A:", trees_encountered(terrain))


# Part B:
# Slopes
# Right 1, down 1.
# Right 3, down 1. (This is the slope you already checked.)
# Right 5, down 1.
# Right 7, down 1.
# Right 1, down 2.

slopes = [(1,1), (3,1), (5,1), (7,1), (1, 2)]

trees = 1
for (right, down) in slopes:
    trees *= trees_encountered(terrain, right, down)

# TODO:
print("Part B:", trees)