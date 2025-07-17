from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models, database
from .database import engine
from .router import post, user, auth, vote

# # tell sqlalchemy to run create statements 
# # -> generate tables when first started up
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"] # * = allow all
# ex: ["https://www.google.com", "https://www.youtube.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# path operation/route
@app.get("/")
def root(): # async optiona;
    print("DB URL:", database.SQLALCHEMY_DATABASE_URL)
    return {"message": "Hi new user in docker bind mount"} 
    #fastapi automatically convert into JSon


