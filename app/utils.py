print(f"app/utils.py package: {__package__}")
#Imports to hash passwords in DB
from passlib.context import CryptContext

#Telling the passlib which hashing alhorithm we use(BCRYPT)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify_password(password:str, password_hash:str):
    return pwd_context.verify(secret=password, hash=password_hash)