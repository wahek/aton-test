from fastapi import FastAPI, Depends
from starlette.staticfiles import StaticFiles

from src.database.requests import patch_client_status
from src.database.schemas import User, Status, Client
from src.auth.auth_app import auth_app
from src.auth.crud import get_clients_by_user
from src.auth.auth import get_current_user

app = FastAPI(title="ATON_test")
app.include_router(auth_app, prefix="/auth", tags=["auth"])

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root(user: User = Depends(get_current_user)):
    return {'clients': await get_clients_by_user(user)}


@app.patch("/users/clients/{INN}/status", response_model=Client)
async def change_client_status(INN: int, status_task: Status, current_user: User = Depends(get_current_user)):
    return await patch_client_status(current_user, INN, status_task)
