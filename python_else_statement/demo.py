# %%
# the if statement
broomstick = "Firebolt"

if broomstick == "Firebolt":
    print("It's the fastest broom in the world! 🧹")
else:
    print("It's good enough.")


# %%
# the for loop
broomsticks = ["Nimbus 2000", "Firebolt", "Comet"]

for broomstick in broomsticks:
    print(broomstick)
# else:
    # print("HIT THE ELSE STATEMENT")



# %%
# for-else practical example
from dataclasses import dataclass

@dataclass
class User:
    name: str
    is_admin: bool

users = [
    User(name="Harry", is_admin=False),
    User(name="Ron", is_admin=False),
    User(name="Hermione", is_admin=True),
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
    User(name="Hermione", is_admin=True),
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
# the while loop
import time

def connect_to_server():
    return "fail" # doomed to fail...

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
# the try-except block
try:
    print("in try block")
    raise ValueError
except ValueError:
    print("in except block - reached a ValueError")







# %%
try:
    print("in try block")
    # raise ValueError
    raise SyntaxError
except ValueError:
    print("in except block - reached a ValueError")
else:
    print("HIT THE ELSE STATEMENT - no ValueError")



# %%
# practical example: database transaction
import sqlite3

conn = sqlite3.connect("test.db")

try:
    cur = conn.execute("INSERT INTO my_table VALUES (?, ?)", (1, "harry"))
except sqlite3.Error as e:
    print(f"Something went wrong: {e}")
    conn.rollback()
else:
    print("Committing data base changes")
    conn.commit()
finally:
    conn.close()

