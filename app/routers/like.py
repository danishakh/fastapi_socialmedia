from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/likes",
    tags=["Likes"]
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like, db: Session = Depends(database.get_db), current_user: dict = Depends(oauth2.get_current_user)):
    # fetch the post
    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {like.post_id} does not exist!")
    
    # try to fetch the like / check if this like exists
    like_query = db.query(models.Like).filter(models.Like.post_id == like.post_id, models.Like.user_id == current_user.id)
    like_found = like_query.first()
    # if we are looking to LIKE the post
    if like.dir == 1:
        if like_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{current_user.name} has already voted on post {like.post_id}")
        new_like = models.Like(post_id = like.post_id, user_id = current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "successfully added like"}
    # else we are looking to REMOVE our LIKE from this post
    else:
        if not like_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like does not exist")

        like_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully removed like"}