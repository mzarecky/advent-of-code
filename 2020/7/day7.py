
import re


def parse_input(x):
    temp = x.split(" contain ")
    outer = temp[0].split(" ")
    inner = temp[1].split(", ")
    if temp[1] == "no other bags.":
        return (outer[0], outer[1]), {(0, ("empty",))}
    return (outer[0], outer[1]), set(map(lambda z: (int(z[0]), (z[1], z[2])), map(lambda y: y.split(" "), inner)))


print(parse_input("wavy turquoise bags contain no other bags."))
print(parse_input("vibrant beige bags contain 4 drab lime bags, 1 muted violet bag, 5 drab plum bags, 5 shiny silver bags."))
print(parse_input("vibrant chartreuse bags contain 2 pale red bags."))


with open("./2020/7/input.txt") as f:
    data = f.readlines()
    data = [parse_input(d.strip()) for d in data]
    data = {k: v for k, v in data}


def has_color(color, input_set):
    return any(map(lambda x: x[1] == color, input_set))


def has_colors(color_list, input_set):
    return any(map(lambda c: has_color(c, input_set), color_list))


# print(has_color(('clear', 'brown'), data[('clear', 'olive')]))
# print(has_colors([('cleard', 'brown'), ('bong','breen'), ('oops','orange')], data[('clear', 'olive')]))

# Part 1
all_colors = set(data.keys())
starting_color = {('shiny', 'gold')}
next_set = set()
previous_set = set(filter(lambda c: has_color(('shiny', 'gold'), data[c]), all_colors))
while True:

    if next_set == previous_set:
        break
    else:
        next_set = set(filter(lambda c: has_colors(previous_set, data[c]), all_colors))
        previous_set = next_set | previous_set
        print(f"New size: {len(next_set)} -> {len(previous_set)}")


# Part 2
def get_bag_size(outer_bag_color, all_bags):
    if outer_bag_color == ('empty',):
        return 1
    num_inner_bags = sum(map(lambda x: x[0], all_bags[outer_bag_color]))
    return num_inner_bags + sum(map(lambda x: x[0] * get_bag_size(x[1], all_bags), all_bags[outer_bag_color]))


aa = get_bag_size(('shiny', 'gold'), data)
print(f"Total number of bags: {aa}")
