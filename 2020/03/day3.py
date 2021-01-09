
import functools

with open("./2020/3/input.txt") as f:
    data = f.readlines()
    data = [d.strip() for d in data]
    nrows = len(data)
    ncols = len(data[0])


def coordinate_generator(size_x, size_y, start_x, start_y, slope_x, slope_y):
    current_x = start_x
    current_y = start_y
    while current_y < size_y:
        if current_y > 0:
            yield (current_y, current_x)
        current_y += slope_y
        current_x = (current_x + slope_x) % size_x
    #raise StopIteration


# Part 1
nrows = len(data)
ncols = len(data[0])
gen = coordinate_generator(ncols, nrows, 0, 0, 3, 1)
num_trees = sum(map(lambda x: 1 if data[x[0]][x[1]] == "#" else 0, gen))
print(f"Hit {num_trees} trees")


# Part 2
def part2(input_data, slope_x, slope_y):
    nrows = len(input_data)
    ncols = len(input_data[0])
    gen = coordinate_generator(ncols, nrows, 0, 0, slope_x, slope_y)
    num_trees = sum(map(lambda x: 1 if input_data[x[0]][x[1]] == "#" else 0, gen))
    print(f"Hit {num_trees} trees")
    return num_trees


my_slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
all_trees = list(map(lambda x: part2(data, x[0], x[1]), my_slopes))
prod_trees = functools.reduce(lambda x, y: x * y, all_trees, 1)
print(f"Product of trees is {prod_trees}")
