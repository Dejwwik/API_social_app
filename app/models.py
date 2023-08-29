print(f"app/models.py package: {__package__}")
#Local imports
from app.database import Base

#Modules import
from sqlalchemy.sql.expression import text
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Relationship

class Post(Base):
    
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    #Creates a new property (class User), automatically fetch user data based on owner_id 
    owner = Relationship("User")


class User(Base):
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    phone_number = Column(String, nullable=True, unique=True)

class Vote(Base):
    
    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)


