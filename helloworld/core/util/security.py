from __future__ import annotations

import random
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return password_hash.decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def generate_otp(length: int = 6):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])
