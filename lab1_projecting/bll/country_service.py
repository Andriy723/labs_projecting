from typing import List, Optional
from dal.interfaces.icountry_repository import ICountryRepository
from models.country import Country


class CountryService:
    def __init__(self, country_repo: ICountryRepository):
        self._country_repo = country_repo

    def add_country(self, country_data: dict) -> Country:
        if self._country_repo.get_by_name(country_data['name']):
            raise ValueError("Country with this name already exists")
        return self._country_repo.create(country_data)

    def get_country(self, country_id: int) -> Optional[Country]:
        return self._country_repo.get_by_id(country_id)

    def get_country_by_name(self, name: str) -> Optional[Country]:
        return self._country_repo.get_by_name(name)

    def get_country_by_code(self, code: str) -> Optional[Country]:
        return self._country_repo.get_by_code(code)

    def get_all_countries(self) -> List[Country]:
        return self._country_repo.get_all()