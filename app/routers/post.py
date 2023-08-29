print(f"app/routers/post.py package: {__package__}")
from fastapi import status, HTTPException, Depends, APIRouter
from typing import List, Optional

#Imports to work with POSTGRES
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


#READ
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostOut]) #Get all posts
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user), 
              limit: int = 10, 
              skip: int = 0,
              search: Optional[str] = ""):
    

    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit=limit).offset(offset=skip).all()

    """SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at, posts.owner_id AS posts_owner_id, count(votes.post_id) AS votes
    FROM posts LEFT OUTER JOIN votes ON posts.id = votes.post_id GROUP BY posts.id LIMIT %(param_1)s OFFSET %(param_2)s"""
    #param_1 = limit, param_2 = skip

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)\
            .filter(models.Post.title.contains(search)).group_by(models.Post.id).limit(limit=limit).offset(offset=skip).all()
    
    return posts


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostOut) #Get one post by id
def get_post(id:int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):


    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)\
        .filter(models.Post.id == str(id)).group_by(models.Post.id).first()
    
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")

    return post

 
#CREATE
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostCreate) #Create an post
def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    #new_post = models.Post(title=new_post.title, content=new_post.content, published=new_post.published) 

    #Instead of inserting every column value manually (like above) we can use dictionary unpacking to make it do for us. The new_post is pydantic model, so we are sure, that it structured as we want it to be.
    new_post = models.Post(owner_id=current_user.id, **new_post.model_dump()) #Creates a new post and save it just to variable with this values

    db.add(new_post) #Inserts the new_post from step above into database
    db.commit() #Saves the changes (inserting a new post)
    db.refresh(new_post)  #Retreiving data from DB (new_post)


    return new_post


#UPDATE
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostOut)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == str(id)) #generate query, because we cannot update one post directly, but we have to update like (UPDATE posts SET .... WHERE id=id)
    updated_post = post_query.first() #Get a updated_post from query above. There is only one in query because every id is unique

    if not updated_post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found!")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not creator of this post!")
    
    #This updates a current post from query above, with values in post: schemas.PostCreate
    post_query.update(values={**post.model_dump()}, synchronize_session=False)
    db.commit()

    #Get the modified post from db, where we also return a number of votes, we know that this post exists, because we checked it above.
    updated_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)\
        .filter(models.Post.id == str(id)).group_by(models.Post.id).first()
    
    # db.refresh(updated_post) #Return this post from database, equivalent to RETURNING* in SQL statement. 
    return updated_post



#DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    deleted_post = db.query(models.Post).filter(models.Post.id == str(id)).first() #Find the post with id we selected

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")

    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not creator of this post!")
    
    db.delete(deleted_post) #Delete the post we reitreived from query step above, and delete it from db. Then commit to save changes
    db.commit()