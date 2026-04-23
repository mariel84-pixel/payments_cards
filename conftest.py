import pytest
import os
from dotenv import load_dotenv
from api.payments_api import PaymentsAPI

load_dotenv()


@pytest.fixture(scope="session")
def api_config():
    return {
        "base_url": os.getenv("MP_BASE_URL", "https://api.mercadopago.com"),
        "token": os.getenv("MP_ACCESS_TOKEN", "TEST-token"),
        "headers": {
            "Authorization": f"Bearer {os.getenv('MP_ACCESS_TOKEN', 'TEST-token')}",
            "Content-Type": "application/json",
            "X-Idempotency-Key": "test-key-001",
        },
    }


@pytest.fixture(scope="session")
def payments_api(api_config):
    return PaymentsAPI(
        base_url=api_config["base_url"],
        headers=api_config["headers"],
    )


@pytest.fixture
def valid_payment_payload():
    return {
        "transaction_amount": 100.0,
        "token": "ff8080814c11e237014c1ff593b57b4d",
        "description": "Test payment",
        "installments": 1,
        "payment_method_id": "visa",
        "payer": {
            "email": "test@test.com"
        },
    }
