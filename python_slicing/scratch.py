# %%
class MySeq:
    def __getitem__(self, index):
        return index


s = MySeq()

s[1:5]
s[1:5:2]
s[1:5:2, 4]
s[:]
s[:2]

# %%
dir(slice)
help(slice.indices)

slice(None, 2, None).indices(4)

# %%
my_string = "this is amazing"
my_string2 = my_string[:]
id(my_string) == id(my_string2)  # True

my_string[0] = "T"  # str does not support item assignment

# %%
my_list = list("this is amazing")
my_list2 = my_list[:]
id(my_list) == id(my_list2)  # False

my_list[0] = "T"
print(f"{my_list=}")
print(f"{my_list2=}")

# %%
my_set = set("this is amazing")
my_set[:]  # sets are not subscriptable

# %%
my_tuple = tuple("this is amazing")
my_tuple2 = my_tuple[:]
id(my_tuple) == id(my_tuple2)  # True

my_tuple[0] = "T"  # tuple does not support item assignment
print(f"{my_tuple=}")
print(f"{my_tuple2=}")

my_tuple[:]

# %%
grocery_list = ["eggs", "milk", "goldfish", "apples", "ramen noodles"]

grocery_list[0]
grocery_list[:2]
grocery_list[2:4]
grocery_list[-1]

grocery_list[0:4:2]
grocery_list[1::3]

grocery_list[-1]
grocery_list[-3:]
grocery_list[::-1]

# %%
items = [
    (1001, "Nimbus 2000", 500.00, 1),
    (1002, "Cauldron", 20.50, 17),
    (1003, "Chocolate Frogs", 3.75, 127),
]

orders = ""
for order_id, desc, unit_price, quantity in items:
    unit_price_str = f"${unit_price:.2f}"
    orders += f"{order_id:<10}{desc:<25}{unit_price_str:>8}{quantity:>8}\n"
orders = orders[:-1]
print(orders)

# process flat file - boring way
for item in orders.split("\n"):
    print(
        item[:10].strip(),
        item[10:35].strip(),
        float(item[35:43].strip().replace("$", "")),
        item[43:].strip(),
    )

# process flat file - slice way
ORDER_ID = slice(None, 10)
DESCRIPTION = slice(10, 35)
UNIT_PRICE = slice(35, 43)
QUANTITY = slice(43, None)

for item in orders.split("\n"):
    print(
        item[ORDER_ID].strip(),
        item[DESCRIPTION].strip(),
        float(item[UNIT_PRICE].strip().replace("$", "")),
        item[QUANTITY].strip(),
    )
