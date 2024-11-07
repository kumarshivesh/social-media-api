# In this file, I am using a database (i.e., PostgreSQL) and a ORM (i.e., SQLAlchemy) 
# app/main.py
import logging

# Reduce logging verbosity for SQLAlchemy engine
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import post, user, auth, vote
from typing import List
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

origins = [
    "*",
]

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

@app.get("/")
def root():
    return {"message": "Hello World!"}

""" 
import logging

# Reduce logging verbosity
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

from fastapi import FastAPI, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()


# Data model for posts
class Post(BaseModel):
  title: str
  content: str
  published: bool = True


# GET all posts
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    print(db.query(models.Post))
    # SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at FROM posts
    posts = db.query(models.Post).all()
    return posts

# POST a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    print(f"post.model_dump(): {post.model_dump()}")
     # Print the unpacked dictionary 
    unpacked_dict = post.model_dump()
    print(f"**post.model_dump() would unpack as: title={unpacked_dict['title']}, "
          f"content={unpacked_dict['content']}, published={unpacked_dict['published']}")
    new_post = models.Post(**post.model_dump())
     # Printing the unpacked values from the dictionary
    print("**post.model_dump() unpacked:")
    for key, value in post.model_dump().items():
      print(f"{key}={value}")
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Retrieve the full post with id and created_at
    return new_post

# GET a post by ID
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    print(db.query(models.Post).filter(models.Post.id == id))
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    return post

# DELETE a post by ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# UPDATE a post by ID [Using SQLAlchemy's `update()` function]
@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
""" 

""" 
# UPDATE a post by ID [Manually looping through the fields with `setattr()`]
@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    for key, value in updated_post.model_dump().items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)  # Retrieve the updated post with id and created_at
    return post
""" 


# Using Pydantic schema 
""" 
import logging

# Reduce logging verbosity
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

from fastapi import FastAPI, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Pydantic schema for input (create and update)
class PostCreateSchema(BaseModel):
  title: str
  content: str
  published: bool = True

# Pydantic schema for response (includes id and created_at)
class PostSchema(PostCreateSchema):
  id: int
  created_at: datetime

  class Config:
      from_attributes = True

# Test endpoint
@app.get("/sqlalchemy")
def get_posts(db: Session = Depends(get_db)):
  posts = db.query(models.Post)
  print(posts)
  # SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at FROM posts
  return {"data": "successfull"}

# GET all posts
@app.get("/posts", response_model=List[PostSchema])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

# POST a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostSchema)
def create_post(post: PostCreateSchema, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())  # Exclude id and created_at automatically
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Retrieve the full post with id and created_at
    return new_post

# GET a post by ID
@app.get("/posts/{id}", response_model=PostSchema)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    return post

# DELETE a post by ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# UPDATE a post by ID
@app.put("/posts/{id}", response_model=PostSchema)
def update_post(id: int, updated_post: PostCreateSchema, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    for key, value in updated_post.model_dump().items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)  # Retrieve the updated post with id and created_at
    return post
"""