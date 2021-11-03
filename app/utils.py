from passlib.context import CryptContext

# let passlib know that our default hashing algorithm - bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)