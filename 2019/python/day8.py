
import functools


with open("../data/data8.txt") as f:
    data = f.read().strip()

width = 25
height = 6
n = len(data)
num_layers = int(n / width / height)
layer_size = width * height
all_layers = [data[(layer_size*x):(layer_size*(x+1))] for x in range(num_layers)]


def get_layer_counts(layer):
    counts = {"0": 0, "1": 0, "2": 0}
    for j in layer:
        counts[j] += 1
    return counts


# Part 1 ----
all_counts = [get_layer_counts(x) for x in all_layers]
smallest_zero = functools.reduce(lambda x, y: x if x["0"] <= y["0"] else y, all_counts)
print(smallest_zero["1"] * smallest_zero["2"])


# Part 2 ----
def get_layer_code(layers, i):
    for pixel in [x[i] for x in layers]:
        if pixel != "2":
            return pixel
    return "2"


image = [get_layer_code(all_layers, x) for x in range(layer_size)]


def print_image(image, width, height):
    charmap = {"0": " ", "1": "*", "2": " "}
    for i in range(height):
        for j in range(width):
            print(charmap[image[width * i + j]], end="")
        print("")


print_image(image, width, height)
