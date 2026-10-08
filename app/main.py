from fastapi import FastAPI
from app.routes.test import router as test
from app.routes.users import router as users
from app.routes.auth import router as auth
from app.routes.families import router as families

app = FastAPI()

app.include_router(test)
app.include_router(auth)
app.include_router(users)
app.include_router(families)