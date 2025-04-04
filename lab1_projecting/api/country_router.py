from fastapi import APIRouter, Depends, HTTPException
from bll.country_service import CountryService
from dal.repositories.country_repository import CountryRepository
from config import get_db


def create_country_router():
    router = APIRouter()

    @router.post("/")
    async def add_country(country_data: dict, db=Depends(get_db)):
        service = CountryService(CountryRepository(db))
        try:
            country = service.add_country(country_data)
            return {"message": "Country added", "id": country.id}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/")
    async def get_all_countries(db=Depends(get_db)):
        service = CountryService(CountryRepository(db))
        countries = service.get_all_countries()
        return {"countries": countries}

    @router.get("/{country_id}")
    async def get_country(country_id: int, db=Depends(get_db)):
        service = CountryService(CountryRepository(db))
        country = service.get_country(country_id)
        if not country:
            raise HTTPException(status_code=404, detail="Country not found")
        return country

    @router.get("/name/{name}")
    async def get_country_by_name(name: str, db=Depends(get_db)):
        service = CountryService(CountryRepository(db))
        country = service.get_country_by_name(name)
        if not country:
            raise HTTPException(status_code=404, detail="Country not found")
        return country

    @router.get("/code/{code}")
    async def get_country_by_code(code: str, db=Depends(get_db)):
        service = CountryService(CountryRepository(db))
        country = service.get_country_by_code(code)
        if not country:
            raise HTTPException(status_code=404, detail="Country not found")
        return country

    return router