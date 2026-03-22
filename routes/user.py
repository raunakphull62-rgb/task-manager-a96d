from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserCreate, UserUpdate
from auth import get_current_user
from supabase import create_client, Client
from supabase.py import User as SupabaseUser
from supabase.py import Auth as SupabaseAuth
from typing import List

router = APIRouter()

supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)
auth: SupabaseAuth = supabase.auth

@router.get('/users/', response_model=List[User])
async def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.post('/users/', response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    user.password = auth.hash_password(user.password)
    db_user = User(username=user.username, password=user.password, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get('/users/{user_id}', response_model=User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put('/users/{user_id}', response_model=User)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.username:
        db_user.username = user.username
    if user.password:
        db_user.password = auth.hash_password(user.password)
    if user.email:
        db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete('/users/{user_id}')
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}