from datetime import datetime, timedelta
from faker import Faker
import random

fake = Faker("pt_BR")


def generate_random_due_date():
    return (
        (datetime.now() + timedelta(hours=random.randint(1, 24)))
        if (datetime.now() + timedelta(hours=random.randint(1, 24))) > datetime.now()
        else (datetime.now() + timedelta(hours=1))
    )


def generate_random_invoice():
    # Generate a random CPF (Brazilian tax identification number)
    cpf = fake.cpf()

    # Generate a random name
    name = fake.name()

    # Generate a random amount (here set between 1000 and 100000)
    amount = random.randint(1000, 100000)

    # Generate a random due date between 1 and 24 hours from now
    due = generate_random_due_date()
    # Other fixed attributes
    expiration = 0
    fine = 5
    interest = 2.5
    tags = ["immediate"]

    # Construct the invoice dictionary
    invoice = {
        "amount": amount,
        "name": name,
        "tax_id": cpf,
        "due": due,
        "expiration": expiration,
        "fine": fine,
        "interest": interest,
        "tags": tags,
    }

    return invoice
