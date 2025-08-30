from typing import Optional
from database.models import User as UserTable
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from security.JWT_security import get_current_user
from models.postmodel import PostCreate
from database.database import get_db
from database.models import Post

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post('/create_post')
def create_post(post: PostCreate, db: Session = Depends(get_db), user_data: dict = Depends(get_current_user)):
    new_post = Post(title=post.title, content=post.content, user_id=user_data["id"])
    db.add(new_post)
    db.commit()
    return {"message": "Post created successfully"}

@router.put('/alter_post')
def alter_post(post: PostCreate, db: Session = Depends(get_db), user_data: dict = Depends(get_current_user)):
    old_post = db.query(Post).filter(Post.user_id == user_data["id"], Post.title == post.title).first()
    if not old_post:
        return {"message": "Post not found"}
    old_post.title = post.title
    old_post.content = post.content
    db.commit()
    return {"message": "Post updated successfully"}


@router.get('/get_my_posts')
def get_users_posts(title: Optional[str] = None, db: Session = Depends(get_db), user_data: dict = Depends(get_current_user)):
    if title:
        return db.query(Post).filter(Post.title == title, Post.user_id == user_data["id"]).all()
    return db.query(Post).filter(Post.user_id == user_data["id"]).all()


@router.get("/get_user_post")
def get_user_post(
    username: str,
    title: Optional[str] = None,
    db: Session = Depends(get_db)
):
    user = db.query(UserTable).filter(UserTable.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    query = db.query(Post).filter(Post.user_id == user.id)

    if title:
        query = query.filter(Post.title.ilike(f"%{title}%"))  # частичный поиск

    posts = query.all()

    if not posts:
        raise HTTPException(status_code=404, detail="No posts found")

    return posts


@router.delete('/delete_post')
def delete_post(title: str, db: Session = Depends(get_db), user_data: dict = Depends(get_current_user)):
    post = db.query(Post).filter(Post.title == title, Post.user_id == user_data["id"]).first()
    if not post:
        return {"message": "Post not found"}
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}