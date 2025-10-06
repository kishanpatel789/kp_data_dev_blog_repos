# %%
import time
from functools import wraps

# %%
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Helly world"

# %%
# basic decorator without @ syntax
def my_decorator(func):
    def wrapper():
        print("Before function call")
        func()
        print("After function call")
    return wrapper

def my_func():
    print("Hello world")

my_func = my_decorator(my_func)

my_func()

# %%
# basic decorator that runs func
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
# decorator with arguments
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function call")
        func(*args, **kwargs)
        print("After function call")
    return wrapper

# @my_decorator
def my_func(name, *, age):
    print(f"Hello {name}, you are {age} years old")

my_func("Adam", age=30)

my_func

# %%
# decorator with return value
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper

@my_decorator
def my_func(name, *, age):
    print(f"Hello {name}, you are {age} years old")
    return age

my_func("Adam", age=30)

# %%
# more exciting example
# take a function returns a string. make the str uppercase and add !
def yell(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"{result.upper()}!!!"
    return wrapper

#@yell
def cast_spell(spell_name: str) -> str:
    """Aim wand and emit incantation."""
    print("Raising wand...")
    return spell_name

cast_spell("expecto patronum")


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
def cast_spell(spell_name: str) -> str:
    """Aim wand and emit incantation."""
    print("Raising wand...")
    return spell_name

cast_spell
cast_spell.__annotations__
cast_spell.__doc__
#help(my_func)

# %%
# decorator to time functions
def tictoc(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Function {func.__name__} ran in {end-start:.3f} seconds")
    return wrapper

@tictoc
def run_my_show(thing, *, other):
    print(f"I received {thing} and {other}")

run_my_show('hello', other=4)


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


@repeat(3)
def cast_spell(spell_name: str):
    print(spell_name)

cast_spell("Adam")

# %%
# rate limiter
import time

def rate_limit(func):
    last_called = 0
    def wrapper(*args, **kwargs):
        nonlocal last_called
        threshold = 10 # seconds
        now = time.time()
        if now - last_called <= threshold:
            raise Exception(f"Rate limit exceeded; wait {threshold} seconds")
        last_called = now
        return func(*args, **kwargs)
    return wrapper

@rate_limit
def say_hello(name: str):
    print(f"Hello {name}")

say_hello("Adam")

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
