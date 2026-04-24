import uuid 
from faker import Faker

Faker.seed(0)
fake = Faker("es_AR")


class PaymentFactory:

    @staticmethod
    def valid_payload(token: str) -> dict:
        """
        Para esta entrega, definí las cuotas dentro de la Factory para asegurar que los payloads sean realistas. 
        Sin embargo, soy consciente de que esto introduce un acoplamiento de reglas de negocio. 
        En un entorno productivo real, mi propuesta sería extraer estos valores a un archivo de configuración (Data-Driven) o, 
        mejor aún, parametrizar la fábrica para que consuma las cuotas válidas directamente desde un endpoint de c
        onfiguración de la API, evitando así el mantenimiento manual si las condiciones comerciales cambian.
        """
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
