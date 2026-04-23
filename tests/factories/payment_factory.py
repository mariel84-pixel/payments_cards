import uuid
from faker import Faker

Faker.seed(0)
fake = Faker("es_AR")


class PaymentFactory:

    @staticmethod
    def valid_payload(token: str) -> dict:
        return {
            "transaction_amount": round(fake.pyfloat(min_value=1, max_value=10000, right_digits=2), 2),
            "token": token,
            "description": fake.sentence(nb_words=4),
            "installments": fake.random_element([1, 3, 6, 12]),
            "payment_method_id": "master",
            "payer": {
                "email": fake.email(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
            },
            "external_reference": str(uuid.uuid4()),
        }

    @staticmethod
    def payload_sin_email(token: str) -> dict:
        payload = PaymentFactory.valid_payload(token)
        del payload["payer"]["email"]
        return payload

    @staticmethod
    def payload_monto_cero(token: str) -> dict:
        payload = PaymentFactory.valid_payload(token)
        payload["transaction_amount"] = 0
        return payload

    @staticmethod
    def idempotency_key() -> str:
        return str(uuid.uuid4())
