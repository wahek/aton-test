from pydantic import BaseModel, conint
from enum import Enum
from datetime import datetime


class Status(str, Enum):
    inactive = "Не в работе"
    active = "В работе"
    denied = "Отказ"
    finished = "Сделка закрыта"


class User(BaseModel):
    full_name: str
    login: str


class UserInDB(User):
    hashed_password: str


class Client(BaseModel):
    account_number: int
    first_name: str
    second_name: str
    patronymic: str | None
    birth_date: datetime
    INN: conint(gt=100000000000, lt=999999999999)
    responsible_person: User
    status: Status = Status.inactive
