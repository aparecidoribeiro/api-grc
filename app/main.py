from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.test import router as test
from app.routes.users import router as users
from app.routes.auth import router as auth
from app.routes.families import router as families
from app.routes.inventory import router as inventory
from app.routes.inventory_requests import router as inventory_requests
from app.routes.notifications import router as notifications
from app.routes.events import router as events


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test)
app.include_router(auth)
app.include_router(users)
app.include_router(families)
app.include_router(inventory)
app.include_router(inventory_requests)
app.include_router(notifications)
app.include_router(events)