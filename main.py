from fastapi import FastAPI
from database.database import Base, engine
from routers import auth_router, posts_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(posts_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
