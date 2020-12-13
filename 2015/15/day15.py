
import itertools

# Frosting:     capacity 4,  durability -2, flavor 0,  texture 0, calories 5
# Candy:        capacity 0,  durability 5,  flavor -1, texture 0, calories 8
# Butterscotch: capacity -1, durability 0,  flavor 5,  texture 0, calories 6
# Sugar:        capacity 0,  durability 0,  flavor -2, texture 2, calories 1


def score(frosting_tsp, candy_tsp, butterscotch_tsp, sugar_tsp):
    capacity = max(0, 4 * frosting_tsp - butterscotch_tsp)
    durability = max(0, 5 * candy_tsp - 2 * frosting_tsp)
    flavor = max(0, 5 * butterscotch_tsp - candy_tsp - 2 * sugar_tsp)
    texture = max(0, 2 * sugar_tsp)
    calories = 5 * frosting_tsp + 8 * candy_tsp + 6 * butterscotch_tsp + sugar_tsp
    return capacity * durability * flavor * texture, calories


# Part 1
best_score = -1
current_score = -2
current_calories = -2
best_ratio = None
tsp_size = range(1, 98)
for f, c, b in itertools.product(tsp_size, tsp_size, tsp_size):
    s = 100 - f - c - b
    current_score, current_calories = score(f, c, b, s)
    if current_score > best_score:
        print(f"Found Better ratio: ({f},{c},{b},{s}); score = {current_score}")
        best_score = current_score
        best_ratio = (f, c, b, s)

# Part 2
best_score = -1
current_score = -2
current_calories = -2
best_ratio = None
tsp_size = range(1, 98)
for f, c, b in itertools.product(tsp_size, tsp_size, tsp_size):
    s = 100 - f - c - b
    current_score, current_calories = score(f, c, b, s)
    if current_calories == 500 and current_score > best_score:
        print(f"Found Better ratio: ({f},{c},{b},{s}); score = {current_score}")
        best_score = current_score
        best_ratio = (f, c, b, s)
