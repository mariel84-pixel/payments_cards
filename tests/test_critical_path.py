import logging
from typing import Any

import pytest
import requests
from api.payments_api import PaymentsAPI
from tests.factories.payment_factory import PaymentFactory

log = logging.getLogger(__name__)


# TEST_PAY_001
@pytest.mark.smoke
@pytest.mark.usefixtures("require_credentials")
def test_crear_pago_exitoso(payments_api: PaymentsAPI, valid_payment_payload: dict):
    
    """TEST_PAY_001 · Happy Path · P0 (bloqueante)

    Verifica el flujo principal de creación de un pago con tarjeta Mastercard en sandbox.
    El payload es generado por PaymentFactory con datos realistas (monto, cuotas, email, token).

    Criterio de aceptación (README — Casos cubiertos 8/31):
    - La API responde 200 o 201.
    - El body contiene un `id` de pago asignado por MercadoPago.
    - El `status` es uno de los valores válidos del ciclo de vida: approved, in_process, pending.

    Falla bloqueante si: la API no crea el pago o devuelve un status inesperado.
    """

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
def test_consultar_estado_pago(payments_api: PaymentsAPI, valid_payment_payload: dict):
    
    """TEST_PAY_002 · Happy Path · P0 (bloqueante)

    Verifica que un pago recién creado puede ser consultado por su ID y que los datos
    devueltos son consistentes (el ID de la consulta coincide con el ID de la creación).

    Criterio de aceptación (README — Casos cubiertos 8/31):
    - La consulta GET /v1/payments/{id} responde 200.
    - El `id` en el body de la respuesta es idéntico al `id` obtenido al crear el pago.

    Falla bloqueante si: el endpoint de consulta no existe, devuelve 404, o retorna un ID distinto.
    """

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
def test_monto_minimo(payments_api: PaymentsAPI, payload_monto_cero: dict):
    
    """TEST_VAL_001 · Validación Input · P0 (bloqueante)

    Verifica que la API rechaza un pago con `transaction_amount = 0`.
    Un monto de cero no representa una transacción válida y debe ser bloqueado
    antes de cualquier procesamiento financiero.

    Criterio de aceptación (README — Casos cubiertos 8/31):
    - La API responde 400 Bad Request.

    Falla bloqueante si: la API acepta montos de cero o devuelve un status diferente a 400,
    lo que indicaría una vulnerabilidad de validación en el gateway de pagos.
    """

    log.info("Enviando pago con transaction_amount=0")

    response = payments_api.crear_pago(payload_monto_cero)
    log.info("Respuesta: status=%s body=%s", response.status_code, response.json())

    assert response.status_code == 400


# TEST_VAL_002
@pytest.mark.smoke
@pytest.mark.usefixtures("require_credentials")
def test_email_requerido(payments_api: PaymentsAPI, payload_sin_email: dict):
    
    """TEST_VAL_002 · Validación Input · P0 (bloqueante)

    Verifica que la API rechaza un pago cuando el campo `payer.email` está ausente.
    El email del pagador es requerido por MercadoPago para identificar al comprador
    y enviar notificaciones de la transacción.

    Criterio de aceptación (README — Casos cubiertos 8/31):
    - La API responde 400 Bad Request.

    Falla bloqueante si: la API acepta el pago sin email, lo que indicaría que la
    validación de campos obligatorios del pagador no está funcionando correctamente.
    """

    log.info("Enviando pago sin email en payer: payer=%s", payload_sin_email["payer"])

    response = payments_api.crear_pago(payload_sin_email)
    log.info("Respuesta: status=%s body=%s", response.status_code, response.json())

    assert response.status_code == 400


# TEST_SEC_001
@pytest.mark.smoke
@pytest.mark.usefixtures("require_credentials")
def test_token_requerido(payments_api: PaymentsAPI, valid_payment_payload: dict):
    
    """TEST_SEC_001 · Seguridad & Auth · P0 (bloqueante)

    Verifica que la API rechaza cualquier request que no incluya un token de autorización.
    Se envía el header `Authorization` vacío para simular un acceso no autenticado.

    Criterio de aceptación (README — Casos cubiertos 8/31):
    - La API responde 401 Unauthorized.

    Falla bloqueante si: la API procesa un pago sin credenciales, lo que representaría
    una brecha de seguridad crítica — cualquier persona podría crear pagos sin autenticarse.
    """

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
def test_token_invalido(payments_api: PaymentsAPI, valid_payment_payload: dict):
    
    """TEST_SEC_002 · Seguridad & Auth · P0 (bloqueante)

    Verifica que la API rechaza tokens de autorización que no corresponden a ninguna
    credencial válida. Se envía `Bearer token-invalido` para simular un token adulterado
    o expirado.

    Criterio de aceptación (README — Casos cubiertos 8/31):
    - La API responde 401 Unauthorized.

    Falla bloqueante si: la API acepta tokens arbitrarios, lo que indicaría que la
    validación de credenciales no funciona y cualquier string podría usarse como token.
    """

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
def test_https_obligatorio(payments_api: PaymentsAPI):
   
    """TEST_SEC_003 · Seguridad & Auth · P0 (bloqueante) · xfail esperado en sandbox

    Verifica que el servidor de MercadoPago redirige el tráfico HTTP (puerto 80) a HTTPS,
    garantizando que no existe un endpoint inseguro activo.

    Criterio de aceptación (README — Casos cubiertos 8/31):
    - La API responde con un código de redirección: 301, 302 o 308.

    Comportamiento en sandbox / GitHub Actions (ver Nota 3 del README):
    El entorno bloquea conexiones salientes al puerto 80, por lo que el test lanza
    `ConnectTimeout` antes de recibir respuesta. Está marcado con `@pytest.mark.xfail`
    porque ese fallo es conocido y esperado: resultado `xfailed` = comportamiento correcto.
    Si el entorno permite la conexión y la redirección llega, el test pasa como `passed`.
    """

    log.info("Verificando que HTTP redirige a HTTPS")

    response = payments_api.verificar_https()
    log.info("Respuesta: status=%s location=%s",
             response.status_code,
             response.headers.get("Location", "—"))

    assert response.status_code in (301, 302, 308)


# TEST_PAY_003
@pytest.mark.smoke
@pytest.mark.usefixtures("require_credentials")
def test_idempotency_key(payments_api: PaymentsAPI, api_config: dict[str, Any], valid_payment_payload: dict):
    
    """TEST_PAY_003 · Happy Path · P0 (bloqueante)

    Verifica que el header `X-Idempotency-Key` funciona correctamente: dos requests
    idénticos con el mismo key devuelven el mismo `id` de pago, sin crear un cobro duplicado.
    La clave es un UUID generado por PaymentFactory.

    Criterio de aceptación (README — Casos cubiertos 8/31):
    - Ambas llamadas (r1 y r2) retornan el mismo `id` en el body de la respuesta.

    Falla bloqueante si: la API genera dos pagos distintos para el mismo idempotency key,
    lo que representaría un doble cobro — uno de los errores más graves en un sistema de pagos.
    """
    
    idempotency_key = PaymentFactory.idempotency_key()
    log.info("Usando X-Idempotency-Key=%s", idempotency_key)

    headers = {**api_config["headers"], "X-Idempotency-Key": idempotency_key}

    r1 = payments_api.crear_pago_con_headers(valid_payment_payload, headers)
    log.info("Primera llamada: status=%s id=%s", r1.status_code, r1.json().get("id"))

    r2 = payments_api.crear_pago_con_headers(valid_payment_payload, headers)
    log.info("Segunda llamada: status=%s id=%s", r2.status_code, r2.json().get("id"))

    assert r1.json().get("id") == r2.json().get("id")
