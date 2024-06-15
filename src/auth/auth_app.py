from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from src.database.facke import create_client
from src.auth.schemas import Token
from src.database.schemas import User, UserInDB, Client
from .crud import create_user, get_user, verify_password
from .auth import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES

auth_app = APIRouter()


@auth_app.post("/register", response_model=User)
async def register(user: UserInDB):
    user_in_db = await get_user(login=user.login)
    if user_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    await create_user(user)
    return user


@auth_app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(login=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@auth_app.post('/users/new_client', response_model=Client)
async def create_new_client(current_user: User = Depends(get_current_user)):
    return await create_client(current_user)
