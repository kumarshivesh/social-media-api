# app/utils.py
from passlib.context import CryptContext

# Create a PassLib "context". This is what will be used to hash and verify passwords.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
  return pwd_context.hash(password)

def verify(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)