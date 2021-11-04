from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED
from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags=['Users']  # fastAPI docs 
)

# ------------ USERS ROUTES -----------------

# add new user
@router.post("/", status_code=HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the pass
    hashed_pass = utils.hash_password(user.password)
    user.password = hashed_pass

    new_user = models.User(**user.dict())
    # add to db
    db.add(new_user)
    db.commit()
    # retrieve the new post we just created
    db.refresh(new_user)
    return new_user


# get a user
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist!")
    
    return user