# %%
print("hello")


# %%
my_string = "this is amazing"

my_string[:5]

# %%
class MySeq:
    def __getitem__(self, index):
        return index

s = MySeq()

s[1:5]
s[1:5:2]
s[1:5:2, 4]

# %%
dir(slice)
help(slice.indices)

# %%
my_string = "this is amazing"
my_string2 = my_string[:]
id(my_string) == id(my_string2) # True

my_string[0] = "T" # str does not support item assignment

# %%
my_list = list("this is amazing")
my_list2 = my_list[:]
id(my_list) == id(my_list2) # False

my_list[0] = "T"
print(f"{my_list=}")
print(f"{my_list2=}")

# %%
my_set = set("this is amazing")
my_set[:] # sets are not subscriptable

# %%
my_tuple = tuple("this is amazing")
my_tuple2 = my_tuple[:]
id(my_tuple) == id(my_tuple2) # True

my_tuple[0] = "T" # tuple does not support item assignment
print(f"{my_tuple=}")
print(f"{my_tuple2=}")

my_tuple[:]
