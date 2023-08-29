print(f"app/routers/vote.py package: {__package__}")

from fastapi import status, HTTPException, Depends, APIRouter

#Imports to work with POSTGRES
from sqlalchemy.orm import Session

from app import models, schemas, oauth2
from app.database import get_db


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


#CREATE
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_post(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    #Check if post to vote exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")

    
    found_vote = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id).first()

    #Create a vote
    if (vote.dir == 1):
        
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with id {current_user.id} already voted on post with id {vote.post_id}")

        else:

            new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
            db.add(new_vote) 
            db.commit() 
            
            return {"message":"succesfully added vote"}
    
    #Remove a vote
    else:

        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        else:
            db.delete(found_vote)
            db.commit()
        
    
        return {"message":"succesfully deleted vote"}