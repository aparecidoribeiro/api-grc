from fastapi import FastAPI
from app.routes.test import router as test
from app.routes.auth import router as auth

app = FastAPI()

app.include_router(test)
app.include_router(auth)