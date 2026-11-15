"""Password hashing (scrypt, standard library), JWT tokens, and a small login rate limiter."""
import hashlib
import hmac
import os
import secrets
import time
from collections import defaultdict, deque

import jwt

SCRYPT = dict(n=2**14, r=8, p=1, dklen=32)


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, **SCRYPT)
    return f"scrypt${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        _, salt, digest = stored.split("$")
    except ValueError:
        return False
    candidate = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), **SCRYPT)
    return hmac.compare_digest(candidate.hex(), digest)  # constant-time comparison


def jwt_secret() -> str:
    secret = os.environ.get("JWT_SECRET", "")
    if len(secret) < 32:
        raise RuntimeError("Set JWT_SECRET to a random string of at least 32 characters (e.g. python -c 'import secrets; print(secrets.token_hex(32))').")
    return secret


TOKEN_MINUTES = int(os.environ.get("TOKEN_MINUTES", "30"))


def create_token(user_id: int, minutes: int = TOKEN_MINUTES) -> str:
    now = int(time.time())
    return jwt.encode({"sub": str(user_id), "iat": now, "exp": now + minutes * 60}, jwt_secret(), algorithm="HS256")


def decode_token(token: str) -> int:
    payload = jwt.decode(token, jwt_secret(), algorithms=["HS256"], options={"require": ["exp", "sub"]})  # fixed algorithm list
    return int(payload["sub"])


class RateLimiter:
    """Sliding-window limiter kept in memory: at most `limit` attempts per `window` seconds per key.
    Fine for one process; use Redis or a gateway limit when you run several instances."""

    def __init__(self, limit=5, window=60):
        self.limit, self.window, self.hits = limit, window, defaultdict(deque)

    def allow(self, key: str) -> bool:
        now, q = time.monotonic(), self.hits[key]
        while q and now - q[0] > self.window:
            q.popleft()
        if len(q) >= self.limit:
            return False
        q.append(now)
        return True
