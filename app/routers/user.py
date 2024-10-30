from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils # `models.py`, `schemas.py`, `utils.py` are not in the same directory. These three files are in `app` directory. So, first, we have to go one directory up using `..`
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

# POST a User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_post(user: schemas.UserCreate, db: Session = Depends(get_db)):
  # hash the password i.e., `user.password` by `hash` function which we defined in `utils.py` file
  hashed_password = utils.hash(user.password)
  # update the hashed password with password that user provided in the request body
  user.password = hashed_password 

  new_user = models.User(**user.model_dump())
  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  return new_user

# Get a User by ID
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")
  return user