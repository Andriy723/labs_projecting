from fastapi import APIRouter, Depends, HTTPException
from bll.card_service import CardService
from dal.repositories.card_repository import CardRepository
from config import get_db


def create_card_router():
    router = APIRouter()

    @router.post("/")
    async def add_card(card_data: dict, db=Depends(get_db)):
        service = CardService(CardRepository(db))
        try:
            card = service.add_card(card_data)
            return {"message": "Card added", "id": card.id}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/account/{account_id}")
    async def get_account_cards(account_id: int, db=Depends(get_db)):
        service = CardService(CardRepository(db))
        cards = service.get_account_cards(account_id)
        return {"cards": cards}

    @router.put("/{card_id}")
    async def update_card(card_id: int, card_data: dict, db=Depends(get_db)):
        service = CardService(CardRepository(db))
        card = service.update_card(card_id, card_data)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")
        return {"message": "Card updated"}

    @router.post("/validate")
    async def validate_card(card_data: dict, db=Depends(get_db)):
        service = CardService(CardRepository(db))
        is_valid = service.validate_card(
            card_data['cardNumber'],
            card_data['expiryDate'],
            card_data['cvv']
        )
        return {"is_valid": is_valid}

    return router