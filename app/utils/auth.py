from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer
import jwt
import logging
import uuid

from app.core.config import Config


pwd_context = CryptContext(
    schemes=['bcrypt']
)

ACCESS_TOKEN_EXPIRY = 3600
serializer = URLSafeTimedSerializer(secret_key=Config.SECRET_KEY, salt="email-configuration")


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


def create_url_safe_token(data: dict):
    private_key = serializer.dumps(data)
    return private_key


def decode_url_safe_token(private_key: str, max_age=1800):
    try:
        data = serializer.loads(private_key, max_age=max_age)
        return data
    
    except Exception as e:
        logging.error(str(e))
