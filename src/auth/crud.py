# crud.py
from passlib.context import CryptContext
from src.database.config import db
from src.database.schemas import UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(login: str):
    user = await db.users.find_one({"login": login})
    if user:
        return UserInDB(**user)


async def create_user(user: UserInDB):
    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(user.hashed_password)
    await db.users.insert_one(user_dict)
    await db.clients.isert_one({"full_name": user.full_name, "clients": []})
