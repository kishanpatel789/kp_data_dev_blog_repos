grocery_list = ["eggs", "milk", "goldfish", "apples", "ramen noodles"]
#                 0        1        2          3             4

#                -5       -4       -3         -2            -1

# [start:stop:step]

grocery_list[::2]

grocery_list[-4:0:-1]



class MySeq:
    def __getitem__(self, index):
        return index

s = MySeq()

s[1:5]
s[1:5:2]
s[1:5:2, 4]
s[:]
s[:2]
s["A":"K"]  # slice("A", "K", None)
s[4, 6, 1:5]







# examples
grocery_list[0]
grocery_list[2:4]
grocery_list[:2]
grocery_list[-1]

grocery_list[0:4:2]
grocery_list[1::3]

grocery_list[-1]
grocery_list[-3:]
grocery_list[::-1]
