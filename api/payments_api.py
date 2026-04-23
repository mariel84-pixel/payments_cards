import requests


class PaymentsAPI:
    def __init__(self, base_url: str, headers: dict):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(headers)

    def crear_pago(self, payload: dict) -> requests.Response:
        return self.session.post(f"{self.base_url}/v1/payments", json=payload)

    def consultar_pago(self, payment_id: str) -> requests.Response:
        return self.session.get(f"{self.base_url}/v1/payments/{payment_id}")

    def crear_pago_con_headers(self, payload: dict, headers: dict) -> requests.Response:
        return self.session.post(
            f"{self.base_url}/v1/payments",
            json=payload,
            headers=headers,
        )

    def verificar_https(self) -> requests.Response:
        return requests.get(
            "http://api.mercadopago.com/v1/payments",
            allow_redirects=False,
        )
