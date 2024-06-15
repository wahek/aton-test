from pathlib import Path

from fastapi import FastAPI, Depends, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles

from src.database.requests import patch_client_status
from src.database.schemas import User, Status, Client
from src.auth.auth_app import auth_app
from src.auth.crud import get_clients_by_user
from src.auth.auth import get_current_user
from src.template import templates, BASE_DIR

app = FastAPI(title="ATON_test")
app.include_router(auth_app, prefix="/auth", tags=["auth"])

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=Path(BASE_DIR, 'static')), name="static")


@app.get("/")
async def root(user: User = Depends(get_current_user)):
    return {'clients': await get_clients_by_user(user)}


@app.patch("/users/clients/{INN}/status", response_model=Client)
async def change_client_status(INN: int, status_task: Status, current_user: User = Depends(get_current_user)):
    return await patch_client_status(current_user, INN, status_task)


@app.get("/files/", response_class=HTMLResponse)
async def load_file(request: Request):
    items = {'Без коэффициента точности': '', 'Коэффициент точности 1': 0, 'Коэффициент точности 2': 1}
    return templates.TemplateResponse(
        "base.html", {"request": request, 'items': items}
    )
