from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jose import JWTError, jwt


SECRET_KEY = "secret"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        id = payload.get("id")
        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username, "role": role, "id": id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



def set_permission(role: str):
    def permission_checker(user_data: dict = Depends(get_current_user)):
        if user_data['role'] == role:
            return
        raise HTTPException(status_code=403, detail="Forbidden")
    return permission_checker