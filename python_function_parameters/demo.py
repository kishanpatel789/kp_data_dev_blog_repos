# %%
from datetime import datetime 


# %%
def send_log(message, level):
    ts_formatted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts_formatted}] [{level}] {message}")

send_log("Hello World", "INFO")

# %%
send_log("Hello World", "INFO") # positional

send_log(message="Hello World", level="INFO") # keyword

send_log(level="INFO", message="Hello World") # keyword (but different order)

send_log("Hello World", level="INFO") # mixture of positional and keyword


# %%
def send_log(message, / ,level):
    ...

send_log("Hello World", "INFO") # positional

send_log(message="Hello World", level="INFO") # keyword

# %%
def make_point(x, y, /):
    ...

make_point(y=-4, x=5)


# %%
def send_log(message, *, level):
    ...

send_log(message="Hello World", level="INFO") # keyword

send_log("Hello World", "INFO") # positional



# %%
def send_email(to, subject, *, cc, bcc, reply_to, encrypt=False):
    ...

send_email('hermione@hogwarts.edu', 'I love you', 'harry@hogwarts.edu', 'molly@alumni.hogwarts.edu', 'ron@hogwarts.edu')

send_email(
    'hermione@hogwarts.edu', 
    'I love you', 
    cc='harry@hogwarts.edu',
    bcc='molly@alumni.hogwarts.edu',
    reply_to='ron@hogwarts.edu',
)



# %%
def func(x, y, *args):
    print(f"{x=}, {y=}, {args=}")
    print(type(args))

func(1, 2, 3, 4, 5)

# %%
def send_log(*messages, level="INFO"):
    ts_formatted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for message in messages:
        print(f"[{ts_formatted}] [{level}] {message}")

send_log("Start backup", "Mark disk", "Backup complete", level="INFO")






# %%
def func(x, y, **kwargs):
    print(f"{x=}, {y=}, {kwargs=}")
    print(type(kwargs))

func(1, 2, a=3, b=4, c=5)

# %%
def send_log(*messages, level="INFO", **metadata):
    ts_formatted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    meta_str = " ".join(f"{k}={v}" for k, v in metadata.items())
    for message in messages:
        print(f"[{ts_formatted}] [{level}] {message} {meta_str}")

send_log(
    "Disk usage at 85%",
    "Auto-scaling triggered",
    level="WARNING",
    instance="vm-123",
    region="us-east-1",
)
