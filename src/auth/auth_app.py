from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from src.database.fake import create_client
from src.auth.schemas import Token
from src.database.schemas import User, UserInDB, Client
from .crud import create_user, get_user, verify_password
from .auth import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES

from src.template import templates

auth_app = APIRouter()


@auth_app.get('/register')
async def load_registration(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@auth_app.post("/register")
async def register(request: Request, full_name: str = Form(...), login: str = Form(...), hashed_password: str = Form(...)):
    user = UserInDB(full_name=full_name, login=login, hashed_password=hashed_password)
    user_in_db = await get_user(login=user.login)
    if user_in_db:
        return templates.TemplateResponse("registration.html",
                                          {"request": request, "error": "Username already registered"})
    await create_user(user)
    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)


@auth_app.get('/login')
async def load_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@auth_app.post('/login')
async def login(request: Request, login: str = Form(...), hashed_password: str = Form(...)):
    user = await get_user(login=login)
    if not user or not verify_password(hashed_password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Incorrect username or password"})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.login}, expires_delta=access_token_expires)

    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


@auth_app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@auth_app.post('/users/new_client', response_model=Client)
async def create_new_client(current_user: User = Depends(get_current_user)):
    return await create_client(current_user)
