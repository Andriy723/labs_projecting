from abc import ABC, abstractmethod
from typing import List, Optional
from models.country import Country


class ICountryRepository(ABC):
    @abstractmethod
    def create(self, country_data: dict) -> Country:
        pass

    @abstractmethod
    def get_by_id(self, country_id: int) -> Optional[Country]:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Country]:
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Country]:
        pass

    @abstractmethod
    def get_all(self) -> List[Country]:
        pass