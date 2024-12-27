# %%
import base64
from datetime import datetime, timezone, timedelta
import jwt
import json

# %% [markdown]
# # Test encoding and decoding

# %%
# test encoding and decoding
encoded_bytes = base64.b64encode("hello".encode("utf-8"))

decoded_string = base64.b64decode(encoded_bytes.decode("utf-8"))
decoded_string

# %% [markdown]
# # JWT
# - use the `pyjwt` package to create a jwt token
# %%
ACCESS_TOKEN_AUD = "accio-cookies-website"
SECRET_KEY = "c06bcea721636bc2ef625e1bf9308b67b3820f8329403399aaccb6644c0aea67"
SIGNING_ALGORITHM = "HS256"
now = datetime.now(timezone.utc)

payload = {
    "sub": "harry potter",
    "iat": now,
    "exp": now + timedelta(hours=2),
    "nbf": now - timedelta(seconds=5),
    "aud": ACCESS_TOKEN_AUD,
}
encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=SIGNING_ALGORITHM)

encoded_jwt

# %%
payload = jwt.decode(
    encoded_jwt,
    SECRET_KEY,
    algorithms=[SIGNING_ALGORITHM],
    audience=ACCESS_TOKEN_AUD,
)
payload

# %%
encoded_jwt.split(".")

# %%
import json, base64


def base64_urldecode(input_str: str):
    """Convert base-64 encoded string into utf-8 string and print output.
    Assumes input is a JSON object.

    Args:
        input (str): Base-64 encoded string
    """
    input_bytes = input_str.encode("utf-8")

    # apply base-64 padding
    rem = len(input_bytes) % 4
    if rem > 0:
        input_bytes += b"=" * (4 - rem)

    # decode base-64 string and convert to dictionary
    output_str = base64.urlsafe_b64decode(input_bytes).decode("utf-8")
    output_dict = json.loads(output_str)

    print(json.dumps(output_dict, indent=4))


# decode payload
base64_urldecode(
    "eyJzdWIiOiJoYXJyeSBwb3R0ZXIiLCJpYXQiOjE3MzUzMjE1NTUsImV4cCI6MTczNTMyODc1NSwibmJmIjoxNzM1MzIxNTUwLCJhdWQiOiJhY2Npby1jb29raWVzLXdlYnNpdGUifQ"
)

# %%
# decode header
base64_urldecode("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")


# %%
# convert unix timestamp to datetime
def print_timestamp_as_datetime(timestamp: int):
    print(
        datetime.fromtimestamp(timestamp, timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    )


print_timestamp_as_datetime(1735321555)  # iat: 2024-12-27 17:45:55 UTC
print_timestamp_as_datetime(1735328755)  # exp: 2024-12-27 19:45:55 UTC
print_timestamp_as_datetime(1735321550)  # nbf: 2024-12-27 17:45:50 UTC

# %%
