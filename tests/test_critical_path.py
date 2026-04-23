import logging
import pytest
import requests
from tests.factories.payment_factory import PaymentFactory

log = logging.getLogger(__name__)


# TEST_PAY_001
@pytest.mark.smoke
@pytest.mark.usefixtures("require_credentials")
def test_crear_pago_exitoso(payments_api, valid_payment_payload):
    log.info("Enviando payload: monto=%.2f método=%s cuotas=%s",
             valid_payment_payload["transaction_amount"],
             valid_payment_payload["payment_method_id"],
             valid_payment_payload["installments"])

    response = payments_api.crear_pago(valid_payment_payload)
    log.info("Respuesta: status=%s body=%s", response.status_code, response.json())

    assert response.status_code in (200, 201)
    data = response.json()
    assert "id" in data
    assert data["status"] in ("approved", "in_process", "pending")
    log.info("Pago creado: id=%s status=%s", data["id"], data["status"])


# TEST_PAY_002
@pytest.mark.smoke
@pytest.mark.usefixtures("require_credentials")
def test_consultar_estado_pago(payments_api, valid_payment_payload):
    log.info("Creando pago para consulta posterior...")
    create_response = payments_api.crear_pago(valid_payment_payload)
    payment_id = create_response.json().get("id")
    log.info("Pago creado: id=%s status_code=%s", payment_id, create_response.status_code)
    assert payment_id, "La creación del pago no retornó un ID válido"

    log.info("Consultando pago id=%s", payment_id)
    response = payments_api.consultar_pago(payment_id)
    log.info("Respuesta consulta: status=%s id=%s", response.status_code, response.json().get("id"))

    assert response.status_code == 200
    assert response.json()["id"] == payment_id


# TEST_VAL_001
@pytest.mark.smoke
@pytest.mark.usefixtures("require_credentials")
def test_monto_minimo(payments_api, payload_monto_cero):
    log.info("Enviando pago con transaction_amount=0")

    response = payments_api.crear_pago(payload_monto_cero)
    log.info("Respuesta: status=%s body=%s", response.status_code, response.json())

    assert response.status_code == 400


# TEST_VAL_002
@pytest.mark.smoke
@pytest.mark.usefixtures("require_credentials")
def test_email_requerido(payments_api, payload_sin_email):
    log.info("Enviando pago sin email en payer: payer=%s", payload_sin_email["payer"])

    response = payments_api.crear_pago(payload_sin_email)
    log.info("Respuesta: status=%s body=%s", response.status_code, response.json())

    assert response.status_code == 400


# TEST_SEC_001
@pytest.mark.smoke
@pytest.mark.usefixtures("require_credentials")
def test_token_requerido(payments_api, valid_payment_payload):
    log.info("Enviando request con Authorization vacío")

    response = payments_api.crear_pago_con_headers(
        valid_payment_payload,
        {"Authorization": "", "Content-Type": "application/json"},
    )
    log.info("Respuesta: status=%s", response.status_code)

    assert response.status_code == 401


# TEST_SEC_002
@pytest.mark.smoke
@pytest.mark.usefixtures("require_credentials")
def test_token_invalido(payments_api, valid_payment_payload):
    log.info("Enviando request con token inválido")

    response = payments_api.crear_pago_con_headers(
        valid_payment_payload,
        {"Authorization": "Bearer token-invalido", "Content-Type": "application/json"},
    )
    log.info("Respuesta: status=%s", response.status_code)

    assert response.status_code == 401


# TEST_SEC_003
@pytest.mark.smoke
@pytest.mark.xfail(raises=requests.exceptions.ConnectTimeout, reason="El entorno bloquea HTTP puerto 80", strict=False)
def test_https_obligatorio(payments_api):
    log.info("Verificando que HTTP redirige a HTTPS")

    response = payments_api.verificar_https()
    log.info("Respuesta: status=%s location=%s",
             response.status_code,
             response.headers.get("Location", "—"))

    assert response.status_code in (301, 302, 308)


# TEST_PAY_003
@pytest.mark.smoke
@pytest.mark.usefixtures("require_credentials")
def test_idempotency_key(payments_api, api_config, valid_payment_payload):
    idempotency_key = PaymentFactory.idempotency_key()
    log.info("Usando X-Idempotency-Key=%s", idempotency_key)

    headers = {**api_config["headers"], "X-Idempotency-Key": idempotency_key}

    r1 = payments_api.crear_pago_con_headers(valid_payment_payload, headers)
    log.info("Primera llamada: status=%s id=%s", r1.status_code, r1.json().get("id"))

    r2 = payments_api.crear_pago_con_headers(valid_payment_payload, headers)
    log.info("Segunda llamada: status=%s id=%s", r2.status_code, r2.json().get("id"))

    assert r1.json().get("id") == r2.json().get("id")
