# %%
from datetime import datetime 

# %%
def my_func(thing):
    print(thing)

my_func('hello')


# %%
def

# %%
def bad_idea(name, thing=[]):
    thing.append(name)
    data = {'stuff': thing}
    return data

bad_idea('attempt1')
bad_idea('attempt2')

# %%
def func(thing, thing2, /, thing3, *, thing4):
    return

func(1, 2, 3, 4)

# %%
# can't match tuple unpacking/kw unpacking with / and * ?
# SyntaxError: * argument may only appear once
def func(thing, thing2,  *thing3 , *, thing4=True):
    print(f"{thing}")
    print(f"{thing2}")
    print(f"{thing3}")
    print(f"{thing4}")

func(1, 2, 3, 4, 5)

# %%
def func(thing, thing2,  *thing3 , thing4=True):
    print(f"{thing}")
    print(f"{thing2}")
    print(f"{thing3}")
    print(f"{thing4}")

func(1, 2, 3, 4, 5)

# %%
def log_message(message, level):
    ts_formatted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[{ts_formatted}] [{level}] {message}")

log_message("Hello World", "INFO")
