from app.core.config import Config
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
import logging
import uuid


pwd_context = CryptContext(
    schemes=['bcrypt']
)

ACCESS_TOKEN_EXPIRY = 3600


def hash_password(password: str) -> str:
    hash = pwd_context.hash(password)
    return hash


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def create_access_token(data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
    payload = {}
    payload["user"] = data
    payload["exp"] = datetime.now(timezone.utc) + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )
    
    return token


def decode_access_token(token: str) -> dict:
    try:
        token_data = jwt.decode(jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
        return token_data
    
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None

