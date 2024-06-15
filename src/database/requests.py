from src.auth.crud import get_clients
from src.database.schemas import Status, User
from src.database.config import db
from src.auth.auth import get_current_user
from fastapi import HTTPException, status, Header


async def patch_client_status(INN: int, status_task: Status, request):
    user = await get_current_user(request)
    client = await get_clients(INN)
    if dict(user) == client["responsible_person"]:
        await db.clients.update_one({"INN": INN}, {"$set": {"status": status_task}})
        return await get_clients(INN)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not responsible person",
        )
