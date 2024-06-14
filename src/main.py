from fastapi import FastAPI
from src.auth.auth_app import auth_app

app = FastAPI()
app.include_router(auth_app, prefix="/auth", tags=["auth"])

