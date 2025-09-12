# %%
nonlocal thing

# %%
globals()

# %%
from dis import dis
import __main__
__main__.__dict__


# %%
__main__.__builtins__


# %%
def f1():
    x = "hello"
    print(x)

f1()

dis(f1)

# %%
def f1():
    x = "hello"
    print(x)

x  # calling 'x' outside the function!

# %% 
x = "hola"  # define 'x' outside the function
def f2():
    print(x)

f2()

dis(f2)

# %% 
x = "hola"  # define 'x' outside the function
def f3():
    x = "hello"  # define another 'x' inside the function
    print(x)

f3()

dis(f3)

# %% 
def f2():
    print(b)
    b = 2

dis(f2)



# %%
def f_outer():
    x = "hola"
    def f_inner():
        print(f"Printing from inner: {x}")
    f_inner()

    print(f"Printing from outer: {x}")

f_outer()

# %%
def f_outer():
    x = "hola"
    def f_inner():
        x = "hello"
        print(x)
    f_inner()
    print(x)

f_outer()

# %%
x

# %%
# test 3 nested functions
def func1():
    x = 100
    def func2():
        def func3():
             print(x) 
        func3()
    func2()

# not sure why this works; multi-nested scope searches progressively until global scope
# %%
func1()

# %%
# closure test
def get_collector():
    series = []
    def store(x):
        series.append(x)
        return len(series)

    return store

collector = get_collector()


# %%
collector("thing1")
collector("thing2")
collector("thing3")

# %%
collector.__code__.co_freevars
collector.__code__.co_varnames
collector.__closure__[0].cell_contents


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
# global
counter = 0   # here's a global variable

def update_counter():
    counter = counter + 1  # try updating global variable

update_counter()

# %% 
counter = 0

def update_counter():
    global counter   # tell Python we're talking about the global 'counter'
    counter = counter + 1

update_counter()
counter  # check value

# %%
# nonlocal
def get_counter():
    count = 0
    def counter():
        count = count + 1  # try updating variable from enclosing scope
    return counter

update_counter = get_counter()

update_counter()

# %%
def get_counter():
    count = 0
    def counter():
        nonlocal count  # tell Python we want the enclosing 'count'
        count = count + 1
    return counter

update_counter = get_counter()

update_counter()

update_counter.__closure__[0].cell_contents  # check value

# %%
# masking
max(4, 7)  # run the built-in max function

def max():  # create your own function
    print("haha, I'm replacing built-in max function!")

max(4, 7)  # try calling the built-in max function again

del(max)  # delete our custom function

max(4, 7)  # try calling the built-in max function again

