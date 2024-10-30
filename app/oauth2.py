# app/oauth2.py
import jwt  # PyJWT library
from jwt import PyJWTError  # Exception handling
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

# Get settings from environment variables
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
  """Create a JWT access token with expiration."""
  to_encode = data.copy()
  expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})

  # Encode the JWT using PyJWT
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

  return encoded_jwt

def verify_access_token(token: str, credentials_exception):
  """Verify the JWT access token."""
  try:
    # Decode the JWT and retrieve the user ID directly as an integer
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id: int = payload.get("user_id")

    if user_id is None:
      raise credentials_exception

    # No need for conversion; store as integer
    token_data = schemas.TokenData(id=user_id)

  except PyJWTError:
    raise credentials_exception

  return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
  """Retrieve the current user based on the JWT token."""
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )

  # Verify token and get the user ID as an integer
  token_data = verify_access_token(token, credentials_exception)
  user = db.query(models.User).filter(models.User.id == token_data.id).first()
  # Print the unpacked values from user
  #unpacked_str = ', '.join([f"{key}={value}" for key, value in vars(user).items()])
  #print(f"user: {unpacked_str}")
  if not user:
    raise HTTPException(status_code=404, detail="User not found")

  return user