from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import schemas, database, models


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
SECRET_KEY = "01d12d1230239d0sad01230asddasdhhaddfh02913241240s12311wrdfds123s"
# Algorithm
ALGORITHM = "HS256"
# Token Expiration Time
ACCESS_TOKEN_EXPIRE_MINS = 60


def create_access_token(data: dict):
    # copy the payload
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINS)

    # update the copy with the expiration time
    to_encode.update({"exp": expire})

    # create JWT 
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        # decode the payload from our JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # extract the id from the payload
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        # validate TokenData schema
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    # return the user_id
    return token_data


# this will be passed into any path function as a dependency to check if the user is still logged in
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials!", headers={"WWW-Authenticate": "Bearer"})

    # check if token is still valid
    token = verify_access_token(token, credentials_exception)

    # lets get the user based off of the id, and pass that instead wherever this dependency is called
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user