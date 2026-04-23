import uuid
from faker import Faker

fake = Faker("es_AR")


class PaymentFactory:

    @staticmethod
    def valid_payload() -> dict:
        return {
            "transaction_amount": round(fake.pyfloat(min_value=1, max_value=10000, right_digits=2), 2),
            "token": "ff8080814c11e237014c1ff593b57b4d",
            "description": fake.sentence(nb_words=4),
            "installments": fake.random_element([1, 3, 6, 12]),
            "payment_method_id": fake.random_element(["visa", "master", "amex"]),
            "payer": {
                "email": fake.email(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
            },
            "external_reference": str(uuid.uuid4()),
        }

    @staticmethod
    def payload_sin_email() -> dict:
        payload = PaymentFactory.valid_payload()
        payload["payer"] = {}
        return payload

    @staticmethod
    def payload_monto_cero() -> dict:
        payload = PaymentFactory.valid_payload()
        payload["transaction_amount"] = 0
        return payload

    @staticmethod
    def idempotency_key() -> str:
        return str(uuid.uuid4())
