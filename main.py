from fastapi import FastAPI
from config import settings
from database import engine
from routes.task import router as tasks_router
from routes.user import router as users_router
from auth import get_current_active_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title='task-manager',
    description='A REST API for managing tasks',
    version='1.0.0'
)

origins = [
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    error_messages = []
    for error in exc.errors():
        error_messages.append({
            'location': error['loc'],
            'message': error['msg'],
            'type': error['type']
        })
    return JSONResponse(status_code=422, content={'errors': error_messages})

app.include_router(tasks_router)
app.include_router(users_router)

@app.get("/healthcheck")
async def healthcheck():
    return {"message": "Service is up and running"}

@app.get("/protected")
async def protected(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    try:
        payload = get_current_active_user(token)
        return {"message": f"Hello, {payload['sub']}"}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")