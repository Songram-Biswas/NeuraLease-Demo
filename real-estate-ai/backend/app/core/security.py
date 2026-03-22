# from datetime import datetime, timedelta, UTC
# from typing import Any, Union
# from jose import jwt
# import bcrypt
# from app.core.config import settings

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)

# def create_access_token(subject: Union[str, Any]) -> str:
#     expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode = {
#         "exp": expire, 
#         "sub": str(subject), 
#         "type": "access"
#     }
#     encoded_jwt = jwt.encode(
#         to_encode, 
#         settings.SECRET_KEY, 
#         algorithm=settings.ALGORITHM
#     )
#     return encoded_jwt

# def create_refresh_token(subject: Union[str, Any]) -> str:
#     expire = datetime.now(UTC) + timedelta(days=7)
#     to_encode = {
#         "exp": expire, 
#         "sub": str(subject), 
#         "type": "refresh"
#     }
#     return jwt.encode(
#         to_encode, 
#         settings.SECRET_KEY, 
#         algorithm=settings.ALGORITHM
#     )

# def decode_token(token: str, expected_type: str = "access") -> str | None:
#     try:
#         payload = jwt.decode(
#             token, 
#             settings.SECRET_KEY, 
#             algorithms=[settings.ALGORITHM]
#         )
#         if payload.get("type") != expected_type:
#             return None
#         return payload.get("sub")
#     except Exception:
#         return None
import bcrypt
from datetime import datetime, timedelta, UTC
from typing import Any, Union
from jose import jwt
from app.core.config import settings

def hash_password(password: str) -> str:
    # পাসওয়ার্ডকে বাইটে কনভার্ট করে সল্ট দিয়ে হ্যাশ করা
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # প্লেইন পাসওয়ার্ড এবং হ্যাশড পাসওয়ার্ড চেক করা
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_access_token(subject: Union[str, Any]) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "exp": expire, 
        "sub": str(subject), 
        "type": "access"
    }
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any]) -> str:
    expire = datetime.now(UTC) + timedelta(days=7)
    to_encode = {
        "exp": expire, 
        "sub": str(subject), 
        "type": "refresh"
    }
    return jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )