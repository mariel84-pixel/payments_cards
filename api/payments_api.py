import uuid
import requests

DEFAULT_TIMEOUT = 10


class PaymentsAPI:
    def __init__(self, base_url: str, headers: dict, timeout: int = DEFAULT_TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(headers)

    def crear_pago(self, payload: dict) -> requests.Response:
        return self.session.post(
            f"{self.base_url}/v1/payments",
            json=payload,
            headers={"X-Idempotency-Key": str(uuid.uuid4())},
            timeout=self.timeout,
        )

    def consultar_pago(self, payment_id: str) -> requests.Response:
        return self.session.get(f"{self.base_url}/v1/payments/{payment_id}", timeout=self.timeout)

    def crear_pago_con_headers(self, payload: dict, headers: dict) -> requests.Response:
        return self.session.post(
            f"{self.base_url}/v1/payments",
            json=payload,
            headers=headers,
            timeout=self.timeout,
        )

    def verificar_https(self) -> requests.Response:
        http_url = self.base_url.replace("https://", "http://", 1)
        return requests.get(
            f"{http_url}/v1/payments",
            allow_redirects=False,
            timeout=self.timeout,
        )
