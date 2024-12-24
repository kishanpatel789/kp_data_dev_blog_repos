# %%
import base64
from datetime import datetime, timezone, timedelta
import jwt
# %%
encoded_bytes = base64.b64encode('hello'.encode('utf-8'))

decoded_string = base64.b64decode(encoded_bytes.decode('utf-8'))
decoded_string

# %%
'hello'.encode('utf-8')


# %% [markdown]
# # JWT
# - use the `pyjwt` package to create a jwt token
# %%
sub = 'harry'
ACCESS_TOKEN_TTL = timedelta(minutes=30)
ACCESS_TOKEN_NBF_LEEWAY = timedelta(seconds=5)
ACCESS_TOKEN_AUD = 'magic-app'
SECRET_KEY = 'c06bcea721636bc2ef625e1bf9308b67b3820f8329403399aaccb6644c0aea67'
SIGNING_ALGORITHM = 'HS256'
now = datetime.now(timezone.utc)
payload = {
    "sub": sub,
    "iat": now,
    "exp": now + ACCESS_TOKEN_TTL,
    "nbf": now - ACCESS_TOKEN_NBF_LEEWAY,
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
base64.urlsafe_b64decode('eyJzdWIiOiJoYXJyeSIsImlhdCI6MTczNTA3MzYyMiwiZXhwIjoxNzM1MDc1NDIyLCJuYmYiOjE3MzUwNzM2MTcsImF1ZCI6Im1hZ2ljLWFwcCJ9')

# %%
base64.b64encode('hello'.encode('utf-8'))