import pytest
import requests


# TEST_PAY_001
def test_crear_pago_exitoso(api_config, valid_payment_payload):
    response = requests.post(
        f"{api_config['base_url']}/v1/payments",
        json=valid_payment_payload,
        headers=api_config["headers"],
    )
    assert response.status_code in (200, 201)
    data = response.json()
    assert "id" in data
    assert data["status"] in ("approved", "in_process", "pending")


# TEST_PAY_002
def test_consultar_estado_pago(api_config, valid_payment_payload):
    create = requests.post(
        f"{api_config['base_url']}/v1/payments",
        json=valid_payment_payload,
        headers=api_config["headers"],
    )
    payment_id = create.json().get("id")
    assert payment_id

    response = requests.get(
        f"{api_config['base_url']}/v1/payments/{payment_id}",
        headers=api_config["headers"],
    )
    assert response.status_code == 200
    assert response.json()["id"] == payment_id


# TEST_VAL_001
def test_monto_minimo(api_config, valid_payment_payload):
    payload = {**valid_payment_payload, "transaction_amount": 0}
    response = requests.post(
        f"{api_config['base_url']}/v1/payments",
        json=payload,
        headers=api_config["headers"],
    )
    assert response.status_code == 400


# TEST_VAL_002
def test_email_requerido(api_config, valid_payment_payload):
    payload = {**valid_payment_payload, "payer": {}}
    response = requests.post(
        f"{api_config['base_url']}/v1/payments",
        json=payload,
        headers=api_config["headers"],
    )
    assert response.status_code == 400


# TEST_SEC_001
def test_token_requerido(api_config, valid_payment_payload):
    headers = {**api_config["headers"], "Authorization": ""}
    response = requests.post(
        f"{api_config['base_url']}/v1/payments",
        json=valid_payment_payload,
        headers=headers,
    )
    assert response.status_code == 401


# TEST_SEC_002
def test_token_invalido(api_config, valid_payment_payload):
    headers = {**api_config["headers"], "Authorization": "Bearer token-invalido"}
    response = requests.post(
        f"{api_config['base_url']}/v1/payments",
        json=valid_payment_payload,
        headers=headers,
    )
    assert response.status_code == 401


# TEST_SEC_003
def test_https_obligatorio():
    response = requests.get("http://api.mercadopago.com/v1/payments", allow_redirects=False)
    assert response.status_code in (301, 302, 308)


# TEST_PAY_003
def test_idempotency_key(api_config, valid_payment_payload):
    headers = {**api_config["headers"], "X-Idempotency-Key": "idempotency-test-key-abc"}
    r1 = requests.post(
        f"{api_config['base_url']}/v1/payments",
        json=valid_payment_payload,
        headers=headers,
    )
    r2 = requests.post(
        f"{api_config['base_url']}/v1/payments",
        json=valid_payment_payload,
        headers=headers,
    )
    assert r1.json().get("id") == r2.json().get("id")
