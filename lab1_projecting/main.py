from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import engine, Base
from api import (
    user_router,
    account_router,
    transaction_router,
    payment_method_router,
    card_router,
    country_router
)

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # Для розробки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    user_router.create_user_router(),
    prefix="/api/users",
    tags=["Users"]
)

app.include_router(
    account_router.create_account_router(),
    prefix="/api/accounts",
    tags=["Accounts"]
)

app.include_router(
    transaction_router.create_transaction_router(),
    prefix="/api/transactions",
    tags=["Transactions"]
)

app.include_router(
    payment_method_router.create_payment_method_router(),
    prefix="/api/payment-methods",
    tags=["Payment Methods"]
)

app.include_router(
    card_router.create_card_router(),
    prefix="/api/cards",
    tags=["Cards"]
)

app.include_router(
    country_router.create_country_router(),
    prefix="/api/countries",
    tags=["Countries"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
