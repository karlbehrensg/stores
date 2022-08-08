from fastapi import HTTPException, status
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.domain import schemas
from src.domain.models import Worker


class WorkersHandler:
    not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Worker not found",
    )

    def __init__(self, db: Session):
        self.db = db

    async def create_worker(self, worker: schemas.WorkerCreate):
        try:
            new_worker = Worker(
                user_id=worker.user_id,
                store_id=worker.store_id,
                rol_id=worker.rol_id,
            )
            self.db.add(new_worker)
            self.db.commit()
            self.db.refresh(new_worker)
            return new_worker
        except (IntegrityError, UniqueViolation):
            raise HTTPException(
                status_code=400,
                detail="The worker already exists or rol is not valid",
            )
