from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from modules.m1744258408460 import TokenData, UserCreate, User
from models import User as UserModel
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import hashlib
import base64
import os
from jose import jwt, JWTError
from config import get_settings

ALGORITHM = "HS256"
SECRET_KEY = get_settings().SECRET_KEY
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user in the database.
    """
    salt = base64.b64encode(os.urandom(16))
    hashed_password = hashlib.pbkdf2_hmac(
        'sha256',
        user.password.encode(),
        salt,
        1000
    ).hex()

    db_user = UserModel(
        username=user.username,
        password=hashed_password,
        # password=user.password,
        salt=salt.decode(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_user)
    db.commit()
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> User | None:
    """
    Authenticate a user by username and password.
    """
    db_user = db.query(UserModel).filter(UserModel.username == username).first()
    if db_user is None:
        return None
    
    hashed_password = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        db_user.salt.encode(),
        1000
    ).hex()

    if db_user.password != hashed_password:
        return None

    return db_user

def create_access_token(username: str, user_id: int, expires_delta: timedelta) -> str:
    """
    Create a JWT access token.
    """
    expires = datetime.now() + expires_delta
    payload = {
        "sub": username,
        "id": user_id,
        "exp": expires
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """
    Get the current user from the token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise JWTError
        return TokenData(username=username, user_id=user_id)
    except JWTError:
        raise JWTError("Could not validate credentials")


