print(f"app/routers/auth.py package: {__package__}")
from fastapi import status, HTTPException, Depends, APIRouter, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

#Imports DB session to work with POSTGRES
from sqlalchemy.orm import Session
from app import models, schemas, utils, oauth2

#import database session
from app.database import get_db


router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)


#LOGIN (POST)
@router.post("/", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials!")
    
    #Check if password hash from input is same as database password hash
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials!")


    #Create a JWT token and return it
    access_token = oauth2.create_access_token(data={"user_id":user.id})

    return {"access_token": access_token, "token_type": "bearer"} 