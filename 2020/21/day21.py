
import re
import collections
import functools


def parse_input(input_string):
    m = re.match(r"([a-z ]+) [(]contains ([a-z, ]+)[)]$", input_string)
    if m is not None:
        ingredients = m[1].split(" ")
        allergens = m[2].split(", ")
        return ingredients, allergens
    else:
        return [], []


with open('./2020/21/input.txt') as f:
    data = [parse_input(d.strip()) for d in f.readlines()]


class AllergyTable:
    def __init__(self):
        self.allergens = set()
        self.ingredients = set()
        self.ingredient_may_contain = collections.defaultdict(set)
        self.allergen_may_be_in = collections.defaultdict(set)
        self.allergen_rules = collections.defaultdict(list)
        self.allergen_combos = dict()
        self.rules = []

    def reduce_rules(self):
        """Successive set intersection for all potential ingredients"""
        for allergen, food_set_list in self.allergen_rules.items():
            self.allergen_combos[allergen] = functools.reduce(lambda x, y: x & y, food_set_list)

    def finalize_rules(self):
        is_final = all(map(lambda x: len(x) == 1, self.allergen_combos.values()))
        while not is_final:
            known_foods = filter(lambda x: len(x) == 1, self.allergen_combos.values())
            known_foods = functools.reduce(lambda x, y: x | y, known_foods)
            unknown_allergens = list(map(lambda y: y[0], filter(lambda x: len(x[1]) > 1, self.allergen_combos.items())))
            for _ in unknown_allergens:
                self.allergen_combos[_].difference_update(known_foods)

            is_final = all(map(lambda x: len(x) == 1, self.allergen_combos.values()))

    def add_food(self, ingredients, allergens):
        for _ in ingredients:
            self.ingredients.add(_)
            for a in allergens:
                self.ingredient_may_contain[_].add(a)
        for _ in allergens:
            self.allergens.add(_)
            self.allergen_rules[_].append(set(ingredients))
            for i in ingredients:
                self.allergen_may_be_in[_].add(i)
        self.rules.append((ingredients, allergens))

    def validate_rules(self, allergy_map):
        pass


# Part 1
AT = AllergyTable()
for ingredients, allergens in data:
    AT.add_food(ingredients, allergens)
AT.reduce_rules()
AT.finalize_rules()

foods_with_allergens = functools.reduce(lambda x, y: x | y, AT.allergen_combos.values())
s = 0
for i, a in AT.rules:
    s += len(set(i).difference(foods_with_allergens))
print(f"Appearances without allergens: {s}")

# Part 2
temp = sorted(AT.allergen_combos.items()).copy()
cdil = ",".join(list(map(lambda x: x[1].pop(), temp)))
print(cdil)
