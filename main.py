import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database.config import Base, engine
from routers import auth, posts, profile

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/pictures", StaticFiles(directory="pictures"), name="pictures")

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(posts.router)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Initializing FastAPI"""

    return "Hello World"


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
