print(f"app/oauth.py package: {__package__}")
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app import schemas, database, models
from app.config import app_settings

#SECRET KEY
SECRET_KEY=app_settings.secret_key

#Algorithm
ALGO = app_settings.algorithm

#Expiration time of token
ACCESS_TOKEN_EXPIRE_MINUTES = app_settings.access_token_expire_minutes


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    #Need to give key "exp" to be able to use time validating in jtw.decode function. The "exp" key is predefined key name.
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGO)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGO])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(dependency=oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-authenticate": "Bearer"})

    token_data = verify_access_token(token=token, credentials_exception=credentials_exception)
    
    user = db.query(models.User).filter(token_data.id == models.User.id).first()
    return user