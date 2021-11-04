from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db


router = APIRouter(
    tags=['Authentication'] # fastAPI docs
)

# login user
@router.post("/login", response_model=schemas.Token)
# def login(user_creds: schemas.UserLogin, db: Session = Depends(get_db)):
def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):    # lets rather use the utility in the fastapi library
    # OAuth2PasswordRequestForm will make user_creds have 'username' and 'password', so we need to account for that
    logged_in_user = db.query(models.User).filter(models.User.email == user_creds.username).first()     # now you will have to send the user_creds as form-data in postman - try it out

    # user with email doesn't exist
    if not logged_in_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    # incorrect password
    if not utils.verify_password(user_creds.password, logged_in_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a jwt
    access_token = oauth2.create_access_token(data={"user_id": logged_in_user.id})

    # return jwt
    return {"access_token": access_token, "token_type": "bearer"}