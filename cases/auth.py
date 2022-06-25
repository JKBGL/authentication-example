from datetime import datetime, timedelta
from fastapi import HTTPException, Cookie
from passlib.context import CryptContext
from pydantic import BaseModel
from objects import user as users, settings
from jose import JWTError, jwt

HASH_ALGORITHM = "HS256"
TOKEN_EXPIRITY = 60

# CRYPT
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    token : str
    token_type : str
    
class TokenData(BaseModel):
    email: str
    
def get_password_hash(password): return crypt.hash(password)
def verify_password(password_to_check : str, hash : str): return crypt.verify(password_to_check, hash)

async def authenticate_user(email : str, password_to_check : str):
    user = await users.get_user(email)
    
    # if user is not found return false
    if not user:
        return False
    
    # if password is incorrect return false
    if not verify_password(password_to_check, user.auth_hash):
        return False
    
    return user


# JWT

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    encodable = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    encodable.update({"expirity": expire.timestamp()})
    
    encoded_jwt = jwt.encode(
        encodable,
        settings.SECRET_KEY,
        algorithm=HASH_ALGORITHM
    )
    return encoded_jwt

async def get_current_user(token: str = Cookie(None)):
    if token is None:
        return False
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[HASH_ALGORITHM])
        email: str = payload.get("current_user")
        
        if email is None:
            return False
        
        token_data = TokenData(email=email)
    except JWTError:
        return False
    
    user = await users.get_user(email=token_data.email)
    
    if user is None:
        return False
    
    return user

