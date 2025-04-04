import csv
import random
from datetime import datetime
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import SessionLocal, Base, engine
from models.card import Card
from models.account import Account
from models.transaction import Transaction
from models.payment_method import PaymentMethod
from models.country import Country
from models.user import User


def recreate_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("✅ Tables were recreated")


def load_data_from_csv(file_path="data/full_data.csv"):
    if not os.path.exists(file_path):
        print(f"❌ File {file_path} was not found!")
        return

    recreate_tables()

    session = SessionLocal()
    stats = {'users': 0, 'accounts': 0, 'transactions': 0,
             'payment_methods': 0, 'cards': 0, 'countries': 0}

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for i, row in enumerate(reader, 1):
            try:
                country = session.query(Country).filter_by(name=row['countryName']).first()
                if not country:
                    country = Country(
                        name=row['countryName'][:100],
                        currency=row['currency'][:10]
                    )
                    session.add(country)
                    session.commit()
                    stats['countries'] += 1

                user = User(
                    userName=row['userName'][:100],
                    email=row['email'][:255],
                    password=row['password'][:255],
                    phoneNumber=row['phoneNumber'][:20] if row[
                        'phoneNumber'] else f"+380{random.randint(100000000, 999999999)}",
                    isActive=True,
                    accountVerified=False
                )
                session.add(user)
                session.commit()
                stats['users'] += 1

                account = Account(
                    accountNumber=row['accountNumber'][:34],
                    balance=float(row['balance']),
                    currency=row['currency'][:10],
                    userID=user.userID
                )
                session.add(account)
                session.commit()
                stats['accounts'] += 1

                transaction = Transaction(
                    amount=float(row['transactionAmount']),
                    date=datetime.strptime(row['transactionDate'], '%Y-%m-%d %H:%M:%S'),
                    description=row['transactionType'][:255],
                    accountID=account.accountID
                )
                session.add(transaction)
                stats['transactions'] += 1

                payment_method = PaymentMethod(
                    name=row['paymentMethodType'][:50],
                    isDefault=False,
                    userID=user.userID
                )
                session.add(payment_method)
                stats['payment_methods'] += 1

                card = Card(
                    cardNumber=row['cardNumber'][:16],
                    holderName=row['userName'][:100],
                    expiryDate=row['expirationDate'][:5],
                    cvv=row['cvv'][:3],
                    cardType=row['cardType'].upper().replace(" ", "_"),
                    cardIssuer=row['countryName'][:100],
                    issuingCountry=country.id,
                    accountID=account.accountID
                )
                session.add(card)
                stats['cards'] += 1

                session.commit()
                print(f"✅ Row {i} was done good")

            except Exception as e:
                session.rollback()
                print(f"⚠️ Error in a row {i}: {str(e)}")
                continue

    session.close()
    print("\n✅ Loading was done. Stats:")
    for k, v in stats.items():
        print(f"- {k}: {v}")


if __name__ == "__main__":
    load_data_from_csv()