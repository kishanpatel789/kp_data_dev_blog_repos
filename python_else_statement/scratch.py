# %%
broomsticks = ["Nimbus 2000", "Firebolt", "Comet"]

for broomstick in broomsticks:
    print(broomstick)
else:
    print("HIT THE ELSE STATEMENT")


# %%
broomsticks = ["Nimbus 2000", "Firebolt", "Comet"]

for broomstick in broomsticks:
    print(broomstick)
    if broomstick == "Firebolt":
        break
else:
    print("HIT THE ELSE STATEMENT")

# %%
# practical example
from dataclasses import dataclass


@dataclass
class User:
    name: str
    is_admin: bool


users = [
    User(name="Harry", is_admin=False),
    User(name="Ron", is_admin=False),
    # User(name="Hermione", is_admin=True),
]

for user in users:
    if user.is_admin:
        print(f"Found one admin: {user}")
        break
else:
    print("No admin user found!")


# %%
# alt to for-else
users = [
    User(name="Harry", is_admin=False),
    User(name="Ron", is_admin=False),
    # User(name="Hermione", is_admin=True),
]
admin_found = False

for user in users:
    if user.is_admin:
        print(f"Found one admin: {user}")
        admin_found = True
        break

if not admin_found:
    print("No admin user found!")



# %%

while True:
    break
else:
    print(
        "else hit"
    )  # only called if while statement becomes falsey and break is not hit


# %%
counter = 0
while counter < 10:
    counter += 1
    print(counter)
else:
    print("else hit")

# %%
import time

def connect_to_server():
    return "fail"

attempts_made = 0

while attempts_made < 3:
    attempts_made += 1
    print(f"Connecting to server (attempt {attempts_made})...")
    if connect_to_server() == "success":
        print("Connected to server!")
        break
    time.sleep(1) # wait 1 second before trying again
else:
    raise TimeoutError("Failed to connect to server after 3 attempts")

# %%
import time

def connect_to_server():
    return "fail"

attempts_made = 0
success = False

while attempts_made < 3:
    attempts_made += 1
    print(f"Connecting to server (attempt {attempts_made})...")
    if connect_to_server() == "success":
        success = True
        print("Connected to server!")
        break
    time.sleep(1)

if not success:
    raise TimeoutError("Failed to connect to server after 3 attempts")


# %%
print("in try block")
raise ValueError

# %%
try:
    print("in try block")
except:
    print("in except block - something went wrong!")


# %%
try:
    print("in try block")
    raise ValueError # simulate an exception
except:
    print("in except block - something went wrong!")

# %%
try:
    print("in try block")
except ValueError:
    print("in except block - reached a ValueError")
else:
    print("HIT THE ELSE STATEMENT - no ValueError")

# %%
try:
    print("in try block")
    raise ValueError # simulate an exception
except ValueError:
    print("in except block - reached a ValueError")
else:
    print("HIT THE ELSE STATEMENT - no ValueError")

# %%
try:
    with open("file_not_exist.txt", 'r') as f:
        data = f.read()
except FileNotFoundError as e:
    print(e)
else:
    print("File has been processed.")


# %%
import sqlite3

conn = sqlite3.connect("test.db")

try:
    conn.execute("INSERT INTO my_table VALUES (2, 'harry');")
except sqlite3.OperationalError:
    conn.rollback()
else:
    conn.commit()

conn.close()
