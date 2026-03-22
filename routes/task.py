from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models.task import Task
from schemas.task import TaskCreate, TaskUpdate
from auth import get_current_user
from supabase import create_client, Client
from typing import List

supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

router = APIRouter()

@router.get('/tasks/', response_model=List[Task])
async def read_tasks(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.user_id == current_user['id']).all()
    return tasks

@router.post('/tasks/', response_model=Task)
async def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_task = Task(title=task.title, description=task.description, completed=task.completed, user_id=current_user['id'])
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get('/tasks/{task_id}', response_model=Task)
async def read_task(task_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user['id']:
        raise HTTPException(status_code=403, detail="You do not have permission to access this task")
    return task

@router.put('/tasks/{task_id}', response_model=Task)
async def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != current_user['id']:
        raise HTTPException(status_code=403, detail="You do not have permission to access this task")
    db_task.title = task.title
    db_task.description = task.description
    db_task.completed = task.completed
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete('/tasks/{task_id}')
async def delete_task(task_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user['id']:
        raise HTTPException(status_code=403, detail="You do not have permission to access this task")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}