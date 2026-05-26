from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "aiduhadibef9un9ufq92nbcq" #secret string server uses to sign tokens
ALGORITHM = "HS256" #algo standard for JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30 #after 30 min user needs to log in again

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #bcrypt is a specific hashing algo and cryptcontext is passlibs way of setting up which algo to use

def hash_password(password: str): #takes text password and returns hashed version to store in db
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str): #takes plain text and hashed pass, checks if they match
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict): #dict is python data structure, like mini db in memory
    #we are passing in a dict like user id, then adding a expiry
    #then jwt encode takes dict and signs it into token 
    #token gets used later to check signature and expiry hasnt passed
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str): #takes token from inc req, decodes, returns user id if valid. 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            return None
        return user_id
    except JWTError:
        return None