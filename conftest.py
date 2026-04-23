import pytest
import os
from dotenv import load_dotenv
from api.payments_api import PaymentsAPI
from tests.factories.payment_factory import PaymentFactory

load_dotenv()


@pytest.fixture(scope="session")
def api_config():
    return {
        "base_url": os.getenv("MP_BASE_URL", "https://api.mercadopago.com"),
        "token": os.getenv("MP_ACCESS_TOKEN", "TEST-token"),
        "headers": {
            "Authorization": f"Bearer {os.getenv('MP_ACCESS_TOKEN', 'TEST-token')}",
            "Content-Type": "application/json",
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
    return PaymentFactory.valid_payload()


@pytest.fixture
def payload_sin_email():
    return PaymentFactory.payload_sin_email()


@pytest.fixture
def payload_monto_cero():
    return PaymentFactory.payload_monto_cero()
