from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.usermodel import User
from security.pass_encryption import hash_password, verify_password
from database.database import get_db
from database.models import User as UserTable
from security.JWT_security import create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post('/register')
def register(user: User, db: Session = Depends(get_db)):
    existing_user = db.query(UserTable).filter(or_(UserTable.username == user.username, UserTable.email == user.email)).first()
    if existing_user:
        return HTTPException(status_code=400, detail="User already exists")
    hashed_password = hash_password(user.password)
    new_user = UserTable(username=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    access_token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/login')
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(user.password)
    existing_user = db.query(UserTable).filter(UserTable.username == user.username).first()
    if not existing_user:
        return HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(user.password, existing_user.password):
        return HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": existing_user.username, "role": existing_user.role, "id": existing_user.id})
    return {"access_token": access_token, "token_type": "bearer"}