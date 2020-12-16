
import re

with open("./2020/16/input.txt") as f:
    data = [d.strip() for d in f.readlines()]
    i = data.index("")
    j = data.index("", i + 1)
    ticket_fields = data[0:i]
    my_ticket = data[i+2]
    other_tickets = data[j+2:]


class TicketScanner:
    def __init__(self, ticket_fields):
        self.fields = {}
        self.field_order = []
        for _ in ticket_fields:
            self.read_field(_)

    def read_field(self, input_string):
        temp = re.split(r"(: |[-]| or )", input_string)
        self.fields[temp[0]] = (int(temp[2]), int(temp[4]), int(temp[6]), int(temp[8]))
        self.field_order.append(temp[0])

    def check_value_in_field(self, field, value):
        w, x, y, z = self.fields[field]
        return w <= value <= x or y <= value <= z

    def check_value_in_any_field(self, value):
        return any(map(lambda x: self.check_value_in_field(x, value), self.field_order))

    @staticmethod
    def parse_ticket(input_string):
        return [int(d) for d in input_string.split(",")]


# Part 1
aa = TicketScanner(ticket_fields)
valid_tickets = []
s = 0
is_valid = False
for t in other_tickets:
    current_ticket = aa.parse_ticket(t)
    is_valid = True
    for v in current_ticket:
        if not aa.check_value_in_any_field(v):
            s += v
            is_valid = False
            break
    if is_valid:
        valid_tickets.append(current_ticket)


# Part 2
tickets = valid_tickets + [aa.parse_ticket(my_ticket)]
num_cols = len(tickets[0])
valid_fields = {c: [] for c in range(num_cols)}

# Which fields are valid for each column in a ticket
for c in range(num_cols):
    # Which fields are valid for each column?
    values = list(map(lambda x: x[c], tickets))
    for field in aa.field_order:
        if all(map(lambda x: aa.check_value_in_field(field, x), values)):
            valid_fields[c].append(field)

# Reduce to a unique mapping per column
field_map = {c: "" for c in range(num_cols)}
cp = valid_fields.copy()

temp = list(filter(lambda x: len(cp[x]) == 1, cp))
while len(temp) > 0:
    for c in temp:
        f = cp[c][0]
        field_map[c] = f  # map it
        # remove it from all others
        for oc in cp:
            if f in cp[oc]:
                cp[oc].remove(f)
    temp = list(filter(lambda x: len(cp[x]) == 1, cp))

# Find product of departure fields
mt = aa.parse_ticket(my_ticket)
departure_fields = list(filter(lambda x: x[1].startswith("departure"), field_map.items()))
prod = 1
for i, f in departure_fields:
    prod *= mt[i]

print(f"Product of fields: {prod}")

