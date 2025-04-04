import csv
import random
from faker import Faker
import os

fake = Faker()


def generate_test_data(file_path="data/full_data.csv", num_records=1000):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    def generate_ukrainian_phone():
        prefixes = ['50', '66', '95', '99', '67', '68', '96', '97', '98', '63', '73', '93']
        return f"+380{random.choice(prefixes)}{random.randint(1000000, 9999999)}"

    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = [
            'userName', 'email', 'password', 'phoneNumber',
            'accountNumber', 'balance', 'currency',
            'transactionAmount', 'transactionDate', 'transactionType',
            'paymentMethodType',
            'cardNumber', 'cardType', 'expirationDate', 'cvv',
            'countryName', 'cardIssuer'
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for _ in range(num_records):
            writer.writerow({
                'userName': fake.name(),
                'email': fake.unique.email(),
                'password': fake.password(),
                'phoneNumber': generate_ukrainian_phone(),
                'accountNumber': fake.iban()[:20],
                'balance': round(random.uniform(100, 10000), 2),
                'currency': random.choice(['USD', 'EUR', 'UAH']),
                'transactionAmount': round(random.uniform(10, 5000), 2),
                'transactionDate': fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
                'transactionType': random.choice(['deposit', 'withdrawal', 'transfer']),
                'paymentMethodType': random.choice(['credit_card', 'debit_card', 'bank_transfer']),
                'cardNumber': fake.credit_card_number(),
                'cardType': random.choice(['CREDIT', 'DEBIT', 'PREPARED']),
                'expirationDate': fake.future_date(end_date='+4y').strftime('%m/%y'),
                'countryName': fake.country(),
                'cardIssuer': 'countryName',
                'cvv': str(random.randint(100, 999))
            })

    print(f"✅ Was generated {num_records} rows in file {file_path}")


if __name__ == "__main__":
    generate_test_data()