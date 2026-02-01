from fastapi import Depends, HTTPException
from database import SessionLocal, User
from security import verify_pwd, create_token, decode_token


def authenticate(username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_pwd(password, user.password):
        return None
    return create_token({"sub": username, "role": user.role})


def get_current_user(token: str):
    try:
        return decode_token(token)
    except:
        raise HTTPException(401, "Invalid token")
