from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from src.adapters.orm import get_db
from src.handlers.workers import WorkersHandler
from src.handlers.stores import StoresHandler
from src.domain import schemas
from src.utils.validation import validate_rol


router = APIRouter(
    prefix="/workers",
    tags=["Workers"],
    responses={404: {"description": "Not found"}},
)


@router.post("", status_code=200, response_model=schemas.WorkerData)
async def create_worker(
    new_worker: schemas.WorkerCreate,
    current_user_id: int = Header(default=None, convert_underscores=True),
    superuser: bool = Header(default=False),
    db: Session = Depends(get_db),
):
    store_handler = StoresHandler(db)
    store = await store_handler.get_store(new_worker.store_id)
    if not store.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The store is not active",
        )
    worker_handler = WorkersHandler(db)

    rol_condition = (
        await validate_rol(
            worker_handler=worker_handler,
            store_id=new_worker.store_id,
            user_id=current_user_id,
            accepted_roles_list=[1],
        )
        if not superuser
        else superuser
    )

    if rol_condition:
        worker = await worker_handler.create_worker(new_worker)
        response = schemas.WorkerData(
            user_id=worker.user_id,
            store_id=worker.store_id,
            store_name=worker.store.name,
            rol_id=worker.rol_id,
            rol_name=worker.rol.name,
            active=worker.active,
        )
        return response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="The user is not authorized",
    )


@router.get("", status_code=200, response_model=schemas.WorkersList)
async def get_workers(
    page: int = 1,
    per_page: int = 10,
    store_id: int = 1,
    current_user_id: int = Header(default=None, convert_underscores=True),
    superuser: bool = Header(default=False),
    db: Session = Depends(get_db),
):
    worker_handler = WorkersHandler(db)
    rol_condition = (
        await validate_rol(
            worker_handler=worker_handler,
            store_id=store_id,
            user_id=current_user_id,
            accepted_roles_list=[1, 2],
        )
        if not superuser
        else superuser
    )

    if rol_condition:
        workers = await worker_handler.get_workers(page, per_page, store_id)
        if not superuser and not workers[0].store.active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The store is not active",
            )
        workers_list = [
            schemas.WorkerBasicData(
                user_id=worker.user_id,
                rol_id=worker.rol_id,
                rol_name=worker.rol.name,
                active=worker.active,
            )
            for worker in workers
        ]
        try:
            response = schemas.WorkersList(
                store_id=store_id,
                store_name=workers[0].store.name,
                store_active=workers[0].store.active,
                workers=workers_list,
            )
        except IndexError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The store does not have workers",
            )
        return response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="The user is not authorized",
    )


@router.get("/{store_id}/{user_id}", status_code=200, response_model=schemas.WorkerData)
async def get_worker(
    store_id: int,
    user_id: int,
    current_user_id: int = Header(default=None, convert_underscores=True),
    superuser: bool = Header(default=False),
    db: Session = Depends(get_db),
):
    worker_handler = WorkersHandler(db)
    rol_condition = (
        await validate_rol(
            worker_handler=worker_handler,
            store_id=store_id,
            user_id=current_user_id,
            accepted_roles_list=[1, 2],
        )
        if not superuser
        else superuser
    )

    if rol_condition:
        worker = await worker_handler.get_worker(store_id, user_id)
        response = schemas.WorkerData(
            user_id=worker.user_id,
            store_id=worker.store_id,
            store_name=worker.store.name,
            rol_id=worker.rol_id,
            rol_name=worker.rol.name,
            active=worker.active,
        )
        return response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="The user is not authorized",
    )


@router.put("/{store_id}/{user_id}", status_code=200, response_model=schemas.WorkerData)
async def update_worker(
    store_id: int,
    user_id: int,
    worker: schemas.WorkerUpdate,
    current_user_id: int = Header(default=None, convert_underscores=True),
    superuser: bool = Header(default=False),
    db: Session = Depends(get_db),
):
    store_handler = StoresHandler(db)
    store = await store_handler.get_store(store_id)
    if not store.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The store is not active",
        )

    worker_handler = WorkersHandler(db)
    rol_condition = (
        await validate_rol(
            worker_handler=worker_handler,
            store_id=store_id,
            user_id=current_user_id,
            accepted_roles_list=[1],
        )
        if not superuser
        else superuser
    )

    if rol_condition:
        worker = await worker_handler.update_worker(store_id, user_id, worker)
        response = schemas.WorkerData(
            user_id=worker.user_id,
            store_id=worker.store_id,
            store_name=worker.store.name,
            rol_id=worker.rol_id,
            rol_name=worker.rol.name,
            active=worker.active,
        )
        return response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="The user is not authorized",
    )


@router.delete(
    "/{store_id}/{user_id}", status_code=200, response_model=schemas.WorkerData
)
async def deactivate_worker(
    store_id: int,
    user_id: int,
    current_user_id: int = Header(default=None, convert_underscores=True),
    superuser: bool = Header(default=False),
    db: Session = Depends(get_db),
):
    store_handler = StoresHandler(db)
    store = await store_handler.get_store(store_id)
    if not store.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The store is not active",
        )

    worker_handler = WorkersHandler(db)

    rol_condition = (
        await validate_rol(
            worker_handler=worker_handler,
            store_id=store_id,
            user_id=current_user_id,
            accepted_roles_list=[1],
        )
        if not superuser
        else superuser
    )

    if rol_condition:
        worker = await worker_handler.deactivate_worker(store_id, user_id)
        response = schemas.WorkerData(
            user_id=worker.user_id,
            store_id=worker.store_id,
            store_name=worker.store.name,
            rol_id=worker.rol_id,
            rol_name=worker.rol.name,
            active=worker.active,
        )
        return response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="The user is not authorized",
    )


@router.post(
    "/{store_id}/{user_id}/activate", status_code=200, response_model=schemas.WorkerData
)
async def activate_worker(
    store_id: int,
    user_id: int,
    current_user_id: int = Header(default=None, convert_underscores=True),
    superuser: bool = Header(default=False),
    db: Session = Depends(get_db),
):
    store_handler = StoresHandler(db)
    store = await store_handler.get_store(store_id)
    if not store.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The store is not active",
        )

    worker_handler = WorkersHandler(db)

    rol_condition = (
        await validate_rol(
            worker_handler=worker_handler,
            store_id=store_id,
            user_id=current_user_id,
            accepted_roles_list=[1],
        )
        if not superuser
        else superuser
    )

    if rol_condition:
        worker = await worker_handler.activate_worker(store_id, user_id)
        response = schemas.WorkerData(
            user_id=worker.user_id,
            store_id=worker.store_id,
            store_name=worker.store.name,
            rol_id=worker.rol_id,
            rol_name=worker.rol.name,
            active=worker.active,
        )
        return response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="The user is not authorized",
    )


@router.delete("/{store_id}/{user_id}/delete", status_code=200)
async def delete_worker(
    store_id: int,
    user_id: int,
    current_user_id: int = Header(default=None, convert_underscores=True),
    superuser: bool = Header(default=False),
    db: Session = Depends(get_db),
):
    store_handler = StoresHandler(db)
    store = await store_handler.get_store(store_id)
    if not store.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The store is not active",
        )

    worker_handler = WorkersHandler(db)

    rol_condition = (
        await validate_rol(
            worker_handler=worker_handler,
            store_id=store_id,
            user_id=current_user_id,
            accepted_roles_list=[1],
        )
        if not superuser
        else superuser
    )

    if rol_condition:
        await worker_handler.delete_worker(store_id, user_id)
        return None

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="The user is not authorized",
    )
