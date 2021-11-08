from os import stat
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List

from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']  # fastAPI docs
)

# ------------ POSTS ROUTES ----------------

#  get all posts
# @router.get("/", response_model=List[schemas.Post])   # imported List from Optional since we are returning a list of Post objects
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # including likes in the response too now!
    # SELECT posts.*, COUNT(likes.post_id) AS likes FROM posts LEFT JOIN likes ON posts.id = likes.post_id GROUP BY posts.id;
    posts = db.query(models.Post, func.count(models.Like.post_id).label("likes")).join(models.Like, models.Post.id == models.Like.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


# add new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    # add the foreign key (user_id) of the current logged in user
    new_post = models.Post(user_id=current_user.id, **post.dict())
    # add to db
    db.add(new_post)
    db.commit()
    # retrieve the new post we just created
    db.refresh(new_post)
    return new_post


# get a post by id
# @router.get("/{id}", response_model=schemas.Post)
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    # including likes in the response
    post = db.query(models.Post, func.count(models.Like.post_id).label("likes")).join(models.Like, models.Post.id == models.Like.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found!")
    return post


# delete a post by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    # if post does not exist
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist!")
    # if post is not current_user's post
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    # synchronize_session=False is some default config, just got it from documentation
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update a post by id
@router.put("/{id}", response_model=schemas.Post)
def updatePost(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    update_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = update_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist!")
    # if post is not current_user's post
    if updated_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    update_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return update_query.first()

