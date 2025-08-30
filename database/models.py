from sqlalchemy.orm import relationship

from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default='user')
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")



class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)