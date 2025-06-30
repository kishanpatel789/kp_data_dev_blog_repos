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
def log_message(message='hello', level):
    ts_formatted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[{ts_formatted}] [{level}] {message}")

log_message("Hello World", "INFO")

# %%
def process_events(events, warnings=[]):  # 🚨 DANGER HERE
    for event in events:
        if "error" in event:
            warnings.append(event)
    return warnings

# 1st batch
events1 = ["ok", "error:missing_field"]
process_events(events1) # expected: ['error:missing_field']

# 2nd batch
events2 = ["error:bad_format"]
process_events(events2) # expected: ['error:bad_format'] ... but we get

# %%
def log_message(message, level):
    ts_formatted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts_formatted}] [{level}] {message}")

log_message("Hello World", "INFO") # positional
log_message(message="Hello World", level="INFO") # keyword
log_message(level="INFO", message="Hello World") # keyword (but different order)
log_message("Hello World", level="INFO") # mixture of positional and keyword

# %%
def make_point(x, y, /):
    ...

make_point(y=-4, x=5)

# %%
def send_email(to, subject, *, cc, bcc, reply_to):
    ...

send_email('hermione@hogwarts.edu', 'I love you', 'harry@hogwarts.edu', 'molly@alumni.hogwarts.edu', 'ron@hogwarts.edu')

send_email('hermione@hogwarts.edu', 'I love you', 
           cc='harry@hogwarts.edu',
           bcc='molly@alumni.hogwarts.edu',
           reply_to='ron@hogwarts.edu')



# %%
def func(x, y, *args):
    print(f"{x=}, {y=}, {args=}")
func(1, 2, 3, 4, 5)

# %%
def log_message(*messages, level="INFO"):
    ts_formatted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for message in messages:
        print(f"[{ts_formatted}] [{level}] {message}")

log_message("Start backup", "Mark disk", level="INFO")


# %%
def func(x, y, **kwargs):
    print(f"{x=}, {y=}, {kwargs=}")

func(1, 2, a=3, b=4, c=5)

# %%
def func(x, *args, y, **kwargs):
    ...

def func(x, y=4, *args, **kwargs):
    ...

def func(**kwargs, x, y=4, *args): # **kwargs must be at end
    ...

# %%
def log_message(*messages, level="INFO", **metadata):
    ts_formatted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    meta_str = " ".join(f"{k}={v}" for k, v in metadata.items())
    for message in messages:
        print(f"[{ts_formatted}] [{level}] {message} {meta_str}")

log_message(
    "Disk usage at 85%",
    "Auto-scaling triggered",
    level="WARNING",
    instance="vm-123",
    region="us-east-1",
)
