# %%
def my_func():
    print("Hello world")

my_func()


# basic decorator
def my_decorator(func):
    def wrapper():
        print("Before function call")
        func()
        print("After function call")
    return wrapper

@my_decorator
def my_func():
    print("Hello world")

my_func()




# %%
# example 1 - passing arguments
def yell(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"{result.upper()}!!!"
    return wrapper

@yell
def cast_spell(spell_name: str) -> str:
    print("Raising wand...")
    return spell_name

cast_spell("expecto patronum")



@yell
def purchase_broom(person: str, price: float, tax: float) -> str:
    """Grab a broom from Diagon Alley"""
    return f"{person} purchased a broom for {price + tax} galleons" 

purchase_broom("Harry", 4, 0.5)




# lost something
purchase_broom
purchase_broom.__doc__
purchase_broom.__annotations__




# %%
# decorator to retain metadata
from functools import wraps

def yell(func):
    @wraps(func)  # pass the original function to @wraps
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"{result.upper()}!!!"
    return wrapper

@yell
def purchase_broom(person: str, price: float, tax: float) -> str:
    """Grab a broom from Diagon Alley"""
    return f"{person} purchased a broom for {price + tax} galleons" 

purchase_broom
purchase_broom.__annotations__
purchase_broom.__doc__




# %%
# example 2: do work before and after function - time function
import time

def tictoc(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter() # log start time
        result = func(*args, **kwargs)       # run original function
        end = time.perf_counter()   # log end time
        print(f"Function '{func.__name__}' ran in {end-start:.3f} seconds")
        return result
    return wrapper




@tictoc
def troublesome_function(name: str):
    time.sleep(3)
    print(f"Hey {name}, I'm done working now!")

troublesome_function("Albus")




# %%
# example 3: keep track of state - rate limiter
import time

def rate_limit(func):
    last_called = 0
    def wrapper(*args, **kwargs):
        nonlocal last_called
        now = time.time()
        if now - last_called <= 10:
            raise Exception("Rate limit exceeded; wait 10 seconds")
        last_called = now
        return func(*args, **kwargs)
    return wrapper

@rate_limit
def call_api(endpoint: str):
    print(f"Calling '{endpoint}'...")

call_api("/owl-post/hedwig")


