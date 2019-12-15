
import typing
import math


class Chemical:
    def __init__(self, name, amt):
        self.name = name
        self.amount = amt

    def __str__(self):
        return f"({self.amount} {self.name})"


class Recipe:
    def __init__(self, recipe: Chemical, inputs: typing.List[Chemical]):
        self.recipe_name = recipe.name
        self.recipe_amount = recipe.amount
        self.inputs = inputs
        self.chemical = recipe
        self.requirements = {x.name for x in inputs}
        self.ore_only = self.requirements == {"ORE"}

    def __str__(self):
        if len(self.inputs) > 1:
            return f"Returns {self.chemical}" + "".join([f"\n----> {x}" for x in self.inputs])
        else:
            return f"Returns {self.chemical}\n----> {self.inputs[0]}"


class Workbench:
    def __init__(self, recipes: typing.List[Recipe], want="FUEL"):
        self.recipes = recipes[:]
        self.recipe_dict: typing.Dict[str, Recipe] = {}           # str: Recipe
        self.base_dict: typing.Dict[str, Recipe] = {}             # str: Recipe
        self.ore_set = set()            # only takes ore to make
        self.compound_set = set()       # takes chemicals and ore to make
        self.resolved = set()

        for j in self.recipes:
            self.recipe_dict[j.recipe_name] = j
            if j.ore_only:
                self.ore_set.add(j.recipe_name)
                # self.base_dict[j.recipe_name] = j
            else:
                self.compound_set.add(j.recipe_name)
                # self.recipe_dict[j.recipe_name] = j

        # Track all chemicals on the workbench
        self.chemical_table = {x: 0 for x in self.compound_set | self.ore_set}
        self.ore_consumed = 0

    def recipe_order(self):
        # Start with fuel, then work down skipping recipes that consume ore
        pass

    def __make(self, c: Chemical, amt: int):
        # print(f"Making {amt} units of {c.name}")
        multiplier = math.ceil(amt / c.amount)
        print(f"Making {c.amount * multiplier} units of {c.name}")

        # Decrement all ingredients from the table
        for i in self.recipe_dict[c.name].inputs:
            print(f"-- Consuming {i.amount * multiplier} units of {i.name}")
            if i.name == "ORE":
                self.ore_consumed += i.amount * multiplier
            else:
                self.chemical_table[i.name] -= multiplier * i.amount
        self.chemical_table[c.name] += multiplier * c.amount
        # input("go")

    def make_chemical_2(self, chemical_name: str, amount: int):
        recipe = self.recipe_dict[chemical_name]

        # Just make it
        self.__make(recipe.chemical, amount)

        # Pay back any negative values
        which_negative = [x for x in self.chemical_table if self.chemical_table[x] < 0]
        while len(which_negative) > 0:
            # print(which_negative)
            print(self.chemical_table)
            # Make recipe of first
            cname = which_negative[0]
            amt = abs(self.chemical_table[cname])
            self.__make(self.recipe_dict[cname].chemical, amt)
            which_negative = [x for x in self.chemical_table if self.chemical_table[x] < 0]

    def make_chemical_3(self, chemical_name: str, amount: int, ore_limit: int = 1000000000000):
        """
        First run returns a chem table that can be replicated every n uses of ore.
        1: Add base chem table to current chem table and n ore uses
        2. Exhaust excess elements that do not consume ore (order by distance from FUEL)
        3. Repeat
        """
        recipe = self.recipe_dict[chemical_name]
        num_fuel = 0
        # Then the chemical table should have one more fuel than necessary
        while True:
            # Make a fuel
            self.__make(recipe.chemical, amount)

            # Pay back any negative values
            which_negative = [x for x in self.chemical_table if self.chemical_table[x] < 0]
            while len(which_negative) > 0:
                print(which_negative)
                print(self.chemical_table)
                # Make recipe of first
                cname = which_negative[0]
                amt = abs(self.chemical_table[cname])
                self.__make(self.recipe_dict[cname].chemical, amt)
                which_negative = [x for x in self.chemical_table if self.chemical_table[x] < 0]
                if self.ore_consumed > ore_limit:
                    break
            if self.ore_consumed > ore_limit:
                break
            num_fuel = self.chemical_table["FUEL"]
        return num_fuel

data = [
    "10 ORE => 10 A",
    "1 ORE => 1 B",
    "7 A, 1 B => 1 C",
    "7 A, 1 C => 1 D",
    "7 A, 1 D => 1 E",
    "7 A, 1 E => 1 FUEL"
]

data2 = [
    "9 ORE => 2 A",
    "8 ORE => 3 B",
    "7 ORE => 5 C",
    "3 A, 4 B => 1 AB",
    "5 B, 7 C => 1 BC",
    "4 C, 1 A => 1 CA",
    "2 AB, 3 BC, 4 CA => 1 FUEL"
]

data3 = [
    "157 ORE => 5 NZVS",
    "165 ORE => 6 DCFZ",
    "44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL",
    "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ",
    "179 ORE => 7 PSHF",
    "177 ORE => 5 HKGWZ",
    "7 DCFZ, 7 PSHF => 2 XJWVT",
    "165 ORE => 2 GPVTF",
    "3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"
]

data4 = [
    "2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG",
    "17 NVRVD, 3 JNWZP => 8 VPVL",
    "53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL",
    "22 VJHF, 37 MNCFX => 5 FWMGM",
    "139 ORE => 4 NVRVD",
    "144 ORE => 7 JNWZP",
    "5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC",
    "5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV",
    "145 ORE => 6 MNCFX",
    "1 NVRVD => 8 CXFTF",
    "1 VJHF, 6 MNCFX => 4 RFSQX",
    "176 ORE => 6 VJHF"
]

data5 = [
    "171 ORE => 8 CNZTR",
    "7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL",
    "114 ORE => 4 BHXH",
    "14 VRPVC => 6 BMBT",
    "6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL",
    "6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT",
    "15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW",
    "13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW",
    "5 BMBT => 4 WPTQ",
    "189 ORE => 9 KTJDG",
    "1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP",
    "12 VRPVC, 27 CNZTR => 2 XDBXC",
    "15 KTJDG, 12 BHXH => 5 XCVML",
    "3 BHXH, 2 VRPVC => 7 MZWV",
    "121 ORE => 7 VRPVC",
    "7 XCVML => 6 RJRHP",
    "5 BHXH, 4 VRPVC => 5 LTCX"
]


def parse_input(x):
    def to_out(y):
        aa = y.split(" ")
        return Chemical(aa[1], int(aa[0]))
    recipe, output = x.split(" => ")
    return Recipe(to_out(output), [to_out(x) for x in recipe.split(", ")])


with open("../data/data14.txt") as f:
    my_data = f.readlines()
    my_data = [x.strip() for x in my_data]


# Part 1 ----
all_recipes = [parse_input(d) for d in my_data]
w = Workbench(all_recipes)
w.make_chemical_2("FUEL", 1)
print(f"Consumed {w.ore_consumed} ore")  # 31


# Part 2 Tests ----
all_recipes = [parse_input(d) for d in data3]
w = Workbench(all_recipes)
w.make_chemical_3("FUEL", 1)
print(f"Consumed {w.ore_consumed} ore")  # 82892753

all_recipes = [parse_input(d) for d in data4]
w = Workbench(all_recipes)
w.make_chemical_3("FUEL", 1)
print(f"Consumed {w.ore_consumed} ore")  # 5586022

all_recipes = [parse_input(d) for d in data5]
w = Workbench(all_recipes)
w.make_chemical_3("FUEL", 1)
print(f"Consumed {w.ore_consumed} ore")  # 460664


# Part 1 Tests ----
all_recipes = [parse_input(d) for d in data]
w = Workbench(all_recipes)
w.make_chemical_2("FUEL", 1)
print(f"Consumed {w.ore_consumed} ore")  # 31

all_recipes = [parse_input(d) for d in data2]
w = Workbench(all_recipes)
w.make_chemical_2("FUEL", 1)
print(f"Consumed {w.ore_consumed} ore")  # 165

all_recipes = [parse_input(d) for d in data3]
w = Workbench(all_recipes)
w.make_chemical_2("FUEL", 1)
print(f"Consumed {w.ore_consumed} ore")  # 13312

all_recipes = [parse_input(d) for d in data4]
w = Workbench(all_recipes)
w.make_chemical_2("FUEL", 1)
print(f"Consumed {w.ore_consumed} ore")  # 180697

all_recipes = [parse_input(d) for d in data5]
w = Workbench(all_recipes)
w.make_chemical_2("FUEL", 1)
print(f"Consumed {w.ore_consumed} ore")  # 2210736
