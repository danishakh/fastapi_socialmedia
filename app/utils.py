from passlib.context import CryptContext

# let passlib know that our default hashing algorithm - bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password):
    return pwd_context.verify(password, hashed_password)