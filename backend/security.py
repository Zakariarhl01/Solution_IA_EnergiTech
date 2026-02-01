from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

SECRET = "SUPER_SECRET_KEY"
ALGO = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])


def hash_pwd(pwd):
    return pwd_context.hash(pwd)


def verify_pwd(pwd, hashed):
    return pwd_context.verify(pwd, hashed)


def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=2)
    return jwt.encode(payload, SECRET, algorithm=ALGO)


def decode_token(token):
    return jwt.decode(token, SECRET, algorithms=[ALGO])
