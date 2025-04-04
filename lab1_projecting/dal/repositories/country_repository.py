from sqlalchemy.orm import Session
from dal.interfaces.icountry_repository import ICountryRepository
from models.country import Country
from config import SessionLocal
from typing import Optional, List


class CountryRepository(ICountryRepository):
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    def create(self, country_data: dict) -> Country:
        country = Country(**country_data)
        self.db.add(country)
        self.db.commit()
        self.db.refresh(country)
        return country

    def get_by_id(self, country_id: int) -> Optional[Country]:
        return self.db.query(Country).filter(Country.id == country_id).first()

    def get_by_name(self, name: str) -> Optional[Country]:
        return self.db.query(Country).filter(Country.name == name).first()

    def get_by_code(self, code: str) -> Optional[Country]:
        return self.db.query(Country).filter(Country.code == code).first()

    def get_all(self) -> List[Country]:
        return self.db.query(Country).all()

    def __del__(self):
        self.db.close()