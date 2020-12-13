
# Sue 18: perfumes: 6, cars: 7, goldfish: 3
class Sue:
    def __init__(self, input_string):
        self.sue_id = None
        self.children = None
        self.cats = None
        self.samoyeds = None
        self.pomeranians = None
        self.akitas = None
        self.vizslas = None
        self.goldfish = None
        self.trees = None
        self.cars = None
        self.perfumes = None
        self.parse_string(input_string)

    def __str__(self):
        return f"{self.sue_id}: chd={self.children}, cat={self.cats}, sam={self.samoyeds}, pom={self.pomeranians}, " + \
            f"akt={self.akitas}, viz={self.vizslas}, gld={self.goldfish}, tree={self.trees}, " + \
            f"car={self.cars}, per={self.perfumes}"

    def parse_string(self, input_string):
        temp = input_string.split(": ", 1)
        attrs = temp[1].split(", ")
        self.sue_id = temp[0]
        for j in attrs:
            temp = j.split(": ")
            setattr(self, temp[0], int(temp[1]))
            # self.set_attr(temp[0], int(temp[1]))

    def set_attr(self, attr_name, attr_value):
        setattr(self, attr_name, attr_value)


# Parse Input
with open("./2015/16/input.txt") as f:
    data = f.readlines()
    all_sues = [Sue(d.strip()) for d in data]


# Find Sue (Part 1)
def check_sue(sue, attribute_name, attribute_value):
    temp = getattr(sue, attribute_name)
    return temp is None or temp == attribute_value


def filter_sues(sue_list, attribute_name, attribute_value):
    return list(filter(lambda x: check_sue(x, attribute_name, attribute_value), sue_list))


my_fav_sues = filter_sues(all_sues, "children", 3)
my_fav_sues = filter_sues(my_fav_sues, "cats", 7)
my_fav_sues = filter_sues(my_fav_sues, "samoyeds", 2)
my_fav_sues = filter_sues(my_fav_sues, "pomeranians", 3)
my_fav_sues = filter_sues(my_fav_sues, "akitas", 0)
my_fav_sues = filter_sues(my_fav_sues, "vizslas", 0)
my_fav_sues = filter_sues(my_fav_sues, "goldfish", 5)
my_fav_sues = filter_sues(my_fav_sues, "trees", 3)
my_fav_sues = filter_sues(my_fav_sues, "cars", 2)
my_fav_sues = filter_sues(my_fav_sues, "perfumes", 1)

for s in my_fav_sues:
    print(s)


# Find Sue (Part 2)
def check_sue2(sue, attribute_name, attribute_value):
    temp = getattr(sue, attribute_name)
    if temp is None:
        return True
    if attribute_name in ["cats", "trees"]:
        return temp > attribute_value
    elif attribute_name in ["pomeranians", "goldfish"]:
        return temp < attribute_value
    else:
        return temp == attribute_value


def filter_sues2(sue_list, attribute_name, attribute_value):
    return list(filter(lambda x: check_sue2(x, attribute_name, attribute_value), sue_list))


my_fav_sues = filter_sues2(all_sues, "children", 3)
my_fav_sues = filter_sues2(my_fav_sues, "cats", 7)
my_fav_sues = filter_sues2(my_fav_sues, "samoyeds", 2)
my_fav_sues = filter_sues2(my_fav_sues, "pomeranians", 3)
my_fav_sues = filter_sues2(my_fav_sues, "akitas", 0)
my_fav_sues = filter_sues2(my_fav_sues, "vizslas", 0)
my_fav_sues = filter_sues2(my_fav_sues, "goldfish", 5)
my_fav_sues = filter_sues2(my_fav_sues, "trees", 3)
my_fav_sues = filter_sues2(my_fav_sues, "cars", 2)
my_fav_sues = filter_sues2(my_fav_sues, "perfumes", 1)

for s in my_fav_sues:
    print(s)
