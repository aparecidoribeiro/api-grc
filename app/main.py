from fastapi import FastAPI
from app.routes.test import router as test
from app.routes.users import router as users

app = FastAPI()

app.include_router(test)
app.include_router(users)