from fastapi import FastAPI
from app.routes.test import router as test
from app.routes.users import router as users
from app.routes.auth import router as auth

app = FastAPI()

app.include_router(test)
app.include_router(users)
app.include_router(auth)