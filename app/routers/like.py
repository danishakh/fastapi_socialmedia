from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/likes",
    tags=["Likes"]
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like, db: Session = Depends(database.get_db), current_user: dict = Depends(oauth2.get_current_user)):
    like_query = db.query(models.Like).filter(models.Like.post_id == like.post_id, models.Like.user_id == current_user.id)
    like_found = like_query.first()
    if like.dir == 1:
        if like_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{current_user.name} has already voted on post {like.post_id}")
        new_like = models.Like(post_id = like.post_id, user_id = current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "successfully added like"}
    else:
        if not like_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like does not exist")

        like_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully removed like"}