print(f"app/routers/user.py package: {__package__}")
from fastapi import status, HTTPException, Depends, APIRouter
from typing import List

#Imports to work with POSTGRES
from sqlalchemy.orm import Session

from app import models, schemas, utils, oauth2
from app.database import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse) #Get one user by id
def get_user(db: Session = Depends(get_db), current_user: models.User= Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    return user



#CREATE
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse) #Create an user
def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.email == new_user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email {new_user.email} already exist!")
    
    #Take inputed password, hash it and assign it to previous password
    new_user.password = utils.hash(new_user.password)
    new_user = models.User(**new_user.model_dump()) #Creates a new user and save it just to variable with this values

    db.add(new_user) #Inserts the new_user from step above into database
    db.commit() #Saves the changes (inserting a new user)
    db.refresh(new_user)  #Retreiving data from DB (new_user)

    return new_user