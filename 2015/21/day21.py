
import itertools
import math


class Equipment:
    def __init__(self, name, cost, damage, armor):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.armor = armor

    def __repr__(self):
        return f"{self.name}: ${self.cost}, D{self.damage}, A{self.armor}"

    def __add__(self, other):
        return Equipment(self.name + "+" + other.name, self.cost + other.cost, self.damage + other.damage, self.armor + other.armor)


weapons = [
    Equipment("dagger", 8, 4, 0),
    Equipment("shortsword", 10, 5, 0),
    Equipment("warhammer", 25, 6, 0),
    Equipment("longsword", 40, 7, 0),
    Equipment("greataxe", 74, 8, 0),
]

armor = [
    Equipment("leather", 13, 0, 1),
    Equipment("chainmail", 31, 0, 2),
    Equipment("splintmail", 53, 0, 3),
    Equipment("bandedmail", 75, 0, 4),
    Equipment("platemail", 102, 0, 5),
    Equipment("No Armor", 0, 0, 0),
]

rings = [
    Equipment("damage +1", 25, 1, 0),
    Equipment("damage +2", 50, 2, 0),
    Equipment("damage +3", 100, 3, 0),
    Equipment("defense +1", 20, 0, 1),
    Equipment("defense +2", 40, 0, 2),
    Equipment("defense +3", 80, 0, 3),
]

special_ring = Equipment("No Ring", 0, 0, 0)

ring_combos = list(itertools.combinations(rings, 2)) + list(map(lambda x: (x, special_ring), rings)) + [(special_ring, special_ring)]

all_equipment_combos = list(itertools.product(weapons, armor, ring_combos))


def game(player_hp, player_damage, player_armor, enemy_hp, enemy_damage, enemy_armor):
    player_hp_loss = max(1, enemy_damage - player_armor)
    enemy_hp_loss = max(1, player_damage - enemy_armor)
    player_turns = math.ceil(player_hp / player_hp_loss)
    enemy_turns = math.ceil(enemy_hp / enemy_hp_loss)
    if player_turns >= enemy_turns:
        return "player"
    else:
        return "enemy"


def play_game(all_equipment_combos, player_hp, enemy_hp=100, enemy_damage=8, enemy_armor=2):
    output = []
    for weapon, armor, rings in all_equipment_combos:
        e = weapon + armor + rings[0] + rings[1]
        winner = game(player_hp, e.damage, e.armor, enemy_hp, enemy_damage, enemy_armor)
        output.append((e.cost, winner))
    return output


all_games = play_game(all_equipment_combos, 100)

# Part 1
temp = min(map(lambda y: y[0], filter(lambda x: x[1] == "player", all_games)))
print(f"Least amount of gold to win: {temp}")

# Part 2
temp = max(map(lambda y: y[0], filter(lambda x: x[1] == "enemy", all_games)))
print(f"Most gold spent to still lose: {temp}")
