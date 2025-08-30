from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Comment, User
from security.JWT_security import set_permission

router = APIRouter(prefix="/admin", tags=["admin"])



@router.delete("/delete_any_comment")
def delete_any_comment(comment_id: int, db: Session = Depends(get_db), permission=Depends(set_permission('admin'))):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    db.delete(comment)
    db.commit()


@router.put("establish_admin")
def establish_admin(username: str, db: Session = Depends(get_db), permission=Depends(set_permission('admin'))):
    user = db.query(User).filter(User.username == username).first()
    user.role = "admin"
    db.commit()