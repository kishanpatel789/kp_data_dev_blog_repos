grocery_list = ["eggs", "milk", "goldfish", "apples", "ramen noodles"]
#                 0        1        2          3             4

#                -5       -4       -3         -2            -1

# [#]
# [start:stop:step]

grocery_list[-2:]


grocery_list[::-1]







class MyCoolSeq:
    def __getitem__(self, index):
        return index

s = MyCoolSeq()

s[0]

s[1:5]

s[1:5:2]

s[:]

s[:2]

s[4, 6, 1:5]











# %%
import string

class SpellBook:
    def __init__(self):
        self.spells = []

    def add_spell(self, incantation):
        self.spells.append(incantation)

    def get_spell_by_first_letter(self, letters):
        search_results = []
        for spell in self.spells:
            if any(spell.startswith(letter) for letter in letters):
                search_results.append(spell)
        return sorted(search_results)

    def __getitem__(self, search_key):
        if isinstance(search_key, str):
            return self.get_spell_by_first_letter(search_key)

        if isinstance(search_key, slice):
            start, stop, step = search_key.start, search_key.stop, search_key.step

            index_start = string.ascii_uppercase.index(start)
            index_stop = string.ascii_uppercase.index(stop) + 1
            range_of_letters = string.ascii_uppercase[index_start:index_stop:step]

            return self.get_spell_by_first_letter(range_of_letters)

# create spell book and add spells
spell_book = SpellBook()
spell_book.add_spell("Flipendo")
spell_book.add_spell("Riddikulus")
spell_book.add_spell("Bombarda")
spell_book.add_spell("Expelliarmus")
spell_book.add_spell("Petrificus Totalus")
spell_book.add_spell("Locomotor Mortis")
spell_book.add_spell("Wingardium Leviosa")

# %%
spell_book["L"]

spell_book["A":"L"]



# %%

string.ascii_uppercase











# %%
# examples
grocery_list[0]
grocery_list[2:4]
grocery_list[:2]

grocery_list[0:4:2]
grocery_list[1::3]

grocery_list[-1]
grocery_list[-3:]
grocery_list[::-1]
