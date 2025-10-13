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



# %
# decorator syntax - alt
my_decorator(my_func)

my_func = my_decorator(my_func)

my_func()


# %%
# more exciting example
# take a function returns a string. make the str uppercase and add !
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

### lost something
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
#help(my_func)

# %%
# decorator to time functions
import time

def tictoc(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter() # log start time
        func(*args, **kwargs)       # run original function
        end = time.perf_counter()   # log end time
        print(f"Function '{func.__name__}' ran in {end-start:.3f} seconds")
    return wrapper

@tictoc
def troublesome_function(name: str):
    time.sleep(5)
    print(f"Hey {name}, I'm done working now!")

troublesome_function("Albus")

# %%
# rate limiter
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

call_api("/owl-post/hedwig") # call again within 10 seconds


# %%
# parameterized decorator - decorator factory
def repeat(num_times: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


@repeat(5)
def cast_spell(spell_name: str):
    print(f"{spell_name.upper()}!!!")

cast_spell("expelliarmus")

# %% 
# filter inputs
def only_ints(func):
    def wrapper(*args, **kwargs):
        list_ints = [arg for arg in args if isinstance(arg, int)]
        value = func(*list_ints, **kwargs)
        return value
    return wrapper

@only_ints
def my_sum(*args):
    value = 0
    for arg in args:
        value += arg
    return value

my_sum(10, 15, 'hello')
