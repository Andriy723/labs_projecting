from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from bll.card_service import CardService
from dal.repositories.card_repository import CardRepository
from config import get_db
from sqlalchemy.orm import Session

from models import Country, Card, Account


class CardCreate(BaseModel):
    accountID: int
    cardNumber: str
    holderName: str
    expiryDate: str
    cvv: str
    cardType: str
    issuingCountry: int

class CardResponse(BaseModel):
    id: int
    cardNumber: str
    holderName: str
    expiryDate: str
    cardType: str
    issuingCountry: int


def create_card_router():
    router = APIRouter()

    @router.post("/", response_model=CardResponse)
    async def create_card(
            card_data: CardCreate,
            db: Session = Depends(get_db)
    ):
        try:
            account = db.query(Account).filter(Account.accountID == card_data.accountID).first()
            if not account:
                raise HTTPException(status_code=404, detail="Account not found")

            country = db.query(Country).filter(Country.id == card_data.issuingCountry).first()
            if not country:
                raise HTTPException(status_code=404, detail="Country not found")

            card = Card(
                accountID=card_data.accountID,
                cardNumber=card_data.cardNumber,
                holderName=card_data.holderName,
                expiryDate=card_data.expiryDate,
                cvv=card_data.cvv,
                cardType=card_data.cardType,
                cardIssuer=country.name,
                issuingCountry=country.id
            )

            db.add(card)
            db.commit()
            db.refresh(card)

            return card
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    @router.post("/cards")
    async def create_card(card_data: CardCreate, db: Session = Depends(get_db)):
        print("Отримані дані:", card_data.dict())

        try:
            country = db.query(Country).get(card_data.issuingCountry)
            if not country:
                raise HTTPException(404, detail="Країну не знайдено")

            card = Card(
                **card_data.dict(),
                cardIssuer=country.name
            )
            db.add(card)
            db.commit()

            return {"message": "Картку успішно створено", "id": card.id}
        except Exception as e:
            db.rollback()
            print("Помилка при створенні картки:", str(e))
            raise HTTPException(400, detail=str(e))

    @router.get("/user/{user_id}")
    async def get_user_cards(user_id: int, db: Session = Depends(get_db)):
        try:
            service = CardService(CardRepository(db))
            cards = service.get_user_cards(user_id)
            return [
                {
                    "id": card.id,
                    "cardNumber": card.cardNumber,
                    "holderName": card.holderName,
                    "expiryDate": card.expiryDate,
                    "cardType": card.cardType,
                    "accountID": card.accountID,
                    "issuingCountry": card.issuingCountry
                }
                for card in cards
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/account/{account_id}")
    async def get_account_cards(account_id: int, db: Session = Depends(get_db)):
        try:
            service = CardService(CardRepository(db))
            cards = service.get_account_cards(account_id)
            return [
                {
                    "id": card.id,
                    "cardNumber": card.cardNumber,
                    "holderName": card.holderName,
                    "expiryDate": card.expiryDate,
                    "cardType": card.cardType,
                    "issuingCountry": card.issuingCountry
                }
                for card in cards
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

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