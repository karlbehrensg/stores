from sqlalchemy.orm import Session

from src.domain.models import Rol


class RolesHandler:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_roles(self):
        return self.db.query(Rol.id, Rol.name).filter_by(active=True).all()
