import asyncio
from datetime import date

from src.database.config import db
from src.database.schemas import Client, User
from random import randint, choice

fake_names = [
    "Александр",
    "Дмитрий",
    "Иван",
    "Сергей",
    "Андрей",
    "Михаил",
    "Алексей",
    "Николай",
    "Владимир",
    "Павел",
    "Юрий",
    "Евгений",
    "Максим",
    "Олег",
    "Виктор",
    "Антон",
    "Роман",
    "Артем",
    "Илья",
    "Кирилл",
]
fake_second = [
    "Иванов",
    "Смирнов",
    "Кузнецов",
    "Попов",
    "Васильев",
    "Петров",
    "Соколов",
    "Михайлов",
    "Новиков",
    "Федоров",
    "Морозов",
    "Волков",
    "Алексеев",
    "Лебедев",
    "Семенов",
    "Егоров",
    "Павлов",
    "Козлов",
    "Степанов",
    "Николаев",
]
fake_patronymic = [
    "Александрович",
    "Дмитриевич",
    "Иванович",
    "Сергеевич",
    "Андреевич",
    "Михайлович",
    "Алексеевич",
    "Николаевич",
    "Владимирович",
    "Павлович",
    "Юрьевич",
    "Евгеньевич",
    "Максимович",
    "Олегович",
    "Викторович",
    "Антонович",
    "Романович",
    "Артемович",
    "Ильич",
    "Кириллович",
]


async def create_client(user: User):
    client = Client(
        account_number=randint(1000000, 9999999),
        first_name=choice(fake_names),
        second_name=choice(fake_second),
        patronymic=choice(fake_patronymic),
        birth_date=date(1990+randint(0, 15), 1+randint(0, 11), 1+randint(0, 27)),
        INN=randint(100000000000, 999999999999),
        responsible_person=user,
    )
    await db.clients.insert_one(client.dict())
    return client


if __name__ == "__main__":
    asyncio.run(create_client(User(full_name="admin", login="admin")))
