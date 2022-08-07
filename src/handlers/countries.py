from sqlalchemy.orm import Session

from src.domain.models import Country


class CountriesHandler:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_countries(self):
        return self.db.query(Country.id, Country.name).filter_by(active=True).all()
