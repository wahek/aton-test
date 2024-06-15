from passlib.context import CryptContext

from src.database.config import db
from src.database.schemas import UserInDB, User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(*args, **kwargs):
    """The function accepts exclusively named arguments, table field names!!!"""
    user = await db.users.find_one({**kwargs})
    if user:
        return UserInDB(**user)


async def create_user(user: UserInDB):
    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(user.hashed_password)
    await db.users.insert_one(user_dict)


async def get_clients_by_user(user: User):
    cursor = db.clients.find({"responsible_person": user.dict()}, {"_id": 0})
    clients = await cursor.to_list(length=None)
    return clients


async def get_clients(INN: int):
    return await db.clients.find_one({"INN": INN})



