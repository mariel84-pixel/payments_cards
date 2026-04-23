import pytest
from api.payments_api import PaymentsAPI
from tests.factories.payment_factory import PaymentFactory


# TEST_PAY_001
def test_crear_pago_exitoso(payments_api, valid_payment_payload):
    response = payments_api.crear_pago(valid_payment_payload)
    assert response.status_code in (200, 201)
    data = response.json()
    assert "id" in data
    assert data["status"] in ("approved", "in_process", "pending")


# TEST_PAY_002
def test_consultar_estado_pago(payments_api, valid_payment_payload):
    payment_id = payments_api.crear_pago(valid_payment_payload).json().get("id")
    assert payment_id

    response = payments_api.consultar_pago(payment_id)
    assert response.status_code == 200
    assert response.json()["id"] == payment_id


# TEST_VAL_001
def test_monto_minimo(payments_api, payload_monto_cero):
    response = payments_api.crear_pago(payload_monto_cero)
    assert response.status_code == 400


# TEST_VAL_002
def test_email_requerido(payments_api, payload_sin_email):
    response = payments_api.crear_pago(payload_sin_email)
    assert response.status_code == 400


# TEST_SEC_001
def test_token_requerido(payments_api, valid_payment_payload):
    response = payments_api.crear_pago_con_headers(
        valid_payment_payload,
        {"Authorization": "", "Content-Type": "application/json"},
    )
    assert response.status_code == 401


# TEST_SEC_002
def test_token_invalido(payments_api, valid_payment_payload):
    response = payments_api.crear_pago_con_headers(
        valid_payment_payload,
        {"Authorization": "Bearer token-invalido", "Content-Type": "application/json"},
    )
    assert response.status_code == 401


# TEST_SEC_003
def test_https_obligatorio(payments_api):
    response = payments_api.verificar_https()
    assert response.status_code in (301, 302, 308)


# TEST_PAY_003
def test_idempotency_key(api_config, valid_payment_payload):
    idempotency_key = PaymentFactory.idempotency_key()
    headers = {**api_config["headers"], "X-Idempotency-Key": idempotency_key}
    api = PaymentsAPI(base_url=api_config["base_url"], headers=headers)

    r1 = api.crear_pago(valid_payment_payload)
    r2 = api.crear_pago(valid_payment_payload)
    assert r1.json().get("id") == r2.json().get("id")
