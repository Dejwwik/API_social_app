print(f"Main.py package: {__package__}")

#venv\Scripts\activate.bat
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

#Local imports
from app.routers import post, user, auth, vote
from app.database import engine

from os import umask, environ

origins = ["https://www.google.com", "*"]

app = FastAPI()

app.add_middleware(middleware_class=
                   CORSMiddleware, 
                   allow_origins = origins,
                   allow_credentials = True,
                   allow_methods = ["*"],
                   allow_headers = ["*"]
                   )

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#Tells sql alchemy to run create statement to create tables in out database, if they do not exist at first startup
#Since we have alembic, there is no need to have this line of code, because alembic will do it for us. :-)
# models.Base.metadata.create_all(bind=engine)


#Run server in localhost
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=environ.get("PORT") if environ.get("PORT") else 8000)
 

