import pytest
import os
import requests as http
from dotenv import load_dotenv
from api.payments_api import PaymentsAPI
from tests.factories.payment_factory import PaymentFactory

load_dotenv()

_DEFAULT_TOKEN = "TEST-token"

_TEST_CARD = {
    "card_number": "5031755734530604",
    "expiration_year": "2030",
    "expiration_month": "11",
    "security_code": "123",
    "cardholder": {
        "name": "APRO",
        "identification": {"type": "DNI", "number": "12345678"},
    },
}


@pytest.fixture(scope="session")
def api_config():
    token = os.getenv("MP_ACCESS_TOKEN", _DEFAULT_TOKEN)
    return {
        "base_url": os.getenv("MP_BASE_URL", "https://api.mercadopago.com"),
        "token": token,
        "headers": {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    }


@pytest.fixture(scope="session")
def require_credentials(api_config):
    if api_config["token"] == _DEFAULT_TOKEN:
        pytest.skip("MP_ACCESS_TOKEN no configurado — se requieren credenciales reales de MercadoPago")


@pytest.fixture(scope="session")
def payments_api(api_config):
    return PaymentsAPI(
        base_url=api_config["base_url"],
        headers=api_config["headers"],
    )


@pytest.fixture
def payment_token(api_config):
    response = http.post(
        f"{api_config['base_url']}/v1/card_tokens",
        headers=api_config["headers"],
        json=_TEST_CARD,
        timeout=10,
    )
    return response.json()["id"]


@pytest.fixture
def valid_payment_payload(payment_token):
    return PaymentFactory.valid_payload(payment_token)


@pytest.fixture
def payload_sin_email(payment_token):
    return PaymentFactory.payload_sin_email(payment_token)


@pytest.fixture
def payload_monto_cero(payment_token):
    return PaymentFactory.payload_monto_cero(payment_token)
