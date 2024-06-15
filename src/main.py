from pathlib import Path

from fastapi import FastAPI, Depends, Request, Form, Header
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles

from src.database.requests import patch_client_status
from src.database.schemas import User, Status, Client
from src.auth.auth_app import auth_app
from src.auth.crud import get_clients_by_user
from src.auth.auth import get_current_user
from src.template import templates, BASE_DIR


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        response = await call_next(request)

        if response.status_code == 401:
            return RedirectResponse(url="/auth/login")

        return response


app = FastAPI(title="ATON_test")
app.include_router(auth_app, prefix="/auth", tags=["auth"])
app.add_middleware(AuthMiddleware)

origins = [
    "http://localhost",
    "http://127.0.0.1",
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
async def root(request: Request, user: User = Depends(get_current_user)):
    print(request.cookies['access_token'])
    return templates.TemplateResponse("clients.html",
                                      {"request": request, 'clients': await get_clients_by_user(User(**user.dict())),
                                       'status': Status})


@app.patch("/users/clients/{INN}/status")
async def change_client_status(INN, status_task, token: str = Header(None)):
    return await patch_client_status(token, INN, status_task)


@app.get("/files/", response_class=HTMLResponse)
async def load_file(request: Request):
    items = {'Без коэффициента точности': '', 'Коэффициент точности 1': 0, 'Коэффициент точности 2': 1}
    return templates.TemplateResponse(
        "base.html", {"request": request, 'items': items}
    )
