from typing import Optional
from security.JWT_security import set_permission
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.models import Comment, Post
from database.database import get_db
from models.commentmodel import CommmentCreate
from security.JWT_security import get_current_user

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post('/create_comment')
def create_comment(new_comment: CommmentCreate, db: Session = Depends(get_db), user_data: dict = Depends(get_current_user)):
    if new_comment.post_id:
        new_comment = Comment(post_id=new_comment.post_id, author_id=user_data["id"], content=new_comment.content)
    elif new_comment.post_title:
        post_id = db.query(Post).filter(Post.title.ilike(f"%{new_comment.post_title}%")).first().id
        new_comment = Comment(post_id=post_id, author_id=user_data["id"], content=new_comment.content)
    db.add(new_comment)
    db.commit()
    return {"message": "Comment created successfully"}

@router.get("/get_my_comments")
def get_my_comments(post_id: Optional[int] = None, post_title: Optional[str] = None, db: Session = Depends(get_db), user_data: dict = Depends(get_current_user)):
    comments = db.query(Comment).filter(Comment.author_id == user_data["id"])
    if post_id:
        comments = comments.filter(Comment.post_id == post_id)
    elif post_title:
        post_id = db.query(Post).filter(Post.title.ilike(f"%{post_title}%")).first().id
        comments = comments.filter(Comment.post_id == post_id)
    return comments.all()


@router.delete('/delete_comment')
def delete_comment(comment_id: int, db: Session = Depends(get_db), user_data: dict = Depends(get_current_user)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment.author_id == user_data["id"]:
        db.delete(comment)
        db.commit()
        return {"message": "Comment deleted successfully"}
    return HTTPException(status_code=403, detail="Forbidden")


@router.delete("/delete_any_comment")
def delete_any_comment(comment_id: int, db: Session = Depends(get_db), permission=Depends(set_permission('admin'))):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    db.delete(comment)
    db.commit()
