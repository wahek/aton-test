from pydantic import BaseModel, constr
from enum import Enum
from datetime import date


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
    second_name: str
    first_name: str
    patronymic: str | None
    birth_date: date
    INN: constr(min_length=12, max_length=12)
    responsible_person: str
    status: Status = Status.inactive
