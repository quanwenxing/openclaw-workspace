"""
Secure password hashing and login using PBKDF2-HMAC (SHA-256).
No third-party dependencies required.
"""

import hashlib
import hmac
import os
import base64


def hash_password(password: str) -> str:
    """Hash a password with a random salt using PBKDF2-HMAC-SHA256."""
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=salt,
        iterations=600_000,  # NIST recommended minimum as of 2024
    )
    # Store salt + hash together, base64-encoded
    return base64.b64encode(salt + key).decode("utf-8")


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify a password against a stored hash. Timing-safe comparison."""
    try:
        decoded = base64.b64decode(stored_hash.encode("utf-8"))
    except Exception:
        return False

    salt = decoded[:32]
    stored_key = decoded[32:]

    candidate_key = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=salt,
        iterations=600_000,
    )
    # Use hmac.compare_digest to prevent timing attacks
    return hmac.compare_digest(stored_key, candidate_key)


# --- In-memory user store (replace with a database in production) ---
_user_store: dict[str, str] = {}  # username -> hashed_password


def register(username: str, password: str) -> bool:
    """Register a new user. Returns False if username already exists."""
    if not username or not password:
        raise ValueError("Username and password must not be empty.")
    if username in _user_store:
        return False
    _user_store[username] = hash_password(password)
    return True


def login(username: str, password: str) -> bool:
    """Authenticate a user. Returns True on success, False otherwise."""
    stored = _user_store.get(username)
    if stored is None:
        # Perform a dummy verify to avoid timing-based username enumeration
        verify_password(password, hash_password("dummy"))
        return False
    return verify_password(password, stored)


# --- Demo ---
if __name__ == "__main__":
    register("alice", "correct-horse-battery-staple")

    print(login("alice", "correct-horse-battery-staple"))  # True
    print(login("alice", "wrong-password"))                # False
    print(login("unknown", "any-password"))                # False
