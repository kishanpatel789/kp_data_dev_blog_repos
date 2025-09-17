# %%
def f1():
    x = "hello"
    print(x)

f1()

# %%
x  # calling 'x' outside the function!

# %% 
x = "hola"  # define 'x' outside the function
def f2():
    print(x)

f2()

# %% 
x = "hola"  # define 'x' outside the function
def f3():
    x = "hello"  # define another 'x' inside the function
    print(x)

f3()


# %%
__builtins__.keys()

# %%
# built-ins whoops
abs

abs(-4)

def abs(x):
    print("haha, I'm replacing built-in abs function!")






# %%
# nested functions
x = 0
def func1():
    x = 100
    def func2():
        x = 200
        print(x)
    func2()

func1()

# closure test
def get_collector():
    series = []
    def store(x):
        series.append(x)
        return len(series)
    return store

collector = get_collector()


# %%
collector("Harry")
collector("Ron")
collector("Hermione")

# %%
collector.__code__.co_freevars
collector.__code__.co_varnames
collector.__closure__[0].cell_contents

# %%
collector2 = get_collector()

collector2("Aang")
collector2("Katara")
collector2("Sokka")

collector.__closure__[0].cell_contents
collector2.__closure__[0].cell_contents


# %%
class Collector():
    def __init__(self):
        self.series = []

    def store(self, x):
        self.series.append(x)
        return len(self.series)

kollector = Collector()

# %%
kollector.store("thing1")
kollector.store("thing2")
kollector.store("thing3")

# %%
kollector.series


# %%
# global attempt 1
counter = 0   # here's a global variable

def update_counter():
    counter = counter + 1  # try updating global variable

update_counter()

# %%
import dis

dis.dis(update_counter)

# %% 
# global attempt 2
counter = 0

def update_counter():
    global counter   # tell Python we're talking about the global 'counter'
    counter = counter + 1

update_counter()

counter  # check value



# %%
TAX_RATE = 0.07  # 7% sales tax

def calculate_total(price):
    return price * (1 + TAX_RATE)

calculate_total(100)

# danger zone
def set_tax_rate(new_rate):
    global TAX_RATE
    TAX_RATE = new_rate  # BAD PRACTICE: mutating global "constant"

set_tax_rate(0.50)

calculate_total(100)





# %%
# nonlocal
def get_counter():
    count = 0
    def update_count():
        count = count + 1  # try updating variable from enclosing scope
    return update_count

update_counter = get_counter()

update_counter()



# %%
def get_counter():
    count = 0
    def update_count():
        nonlocal count  # tell Python we want the enclosing 'count'
        count = count + 1
    return update_count

update_counter = get_counter()

update_counter()

update_counter.__closure__[0].cell_contents  # check value

