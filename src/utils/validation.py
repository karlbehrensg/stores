from fastapi import HTTPException, status

from src.handlers.workers import WorkersHandler


async def validate_rol(
    worker_handler: WorkersHandler,
    store_id: int,
    user_id: int,
    accepted_roles_list: list,
):
    if not isinstance(user_id, int):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user is not valid",
        )

    worker = await worker_handler.get_worker(store_id, user_id)

    if worker and worker.rol_id in accepted_roles_list and worker.active:
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="The user is not authorized",
    )
