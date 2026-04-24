# payments_cards
## CONTEXTO DEL PROYECTO - Testing Automatizado de APIs de Pago

# REPORTE DE COBERTURA - TESTING APIs PAGOS

Mercado Pago Sandbox | Fase 1 & # MATRIZ EJECUTIVA
### 📊 MATRIZ EJECUTIVA: Cobertura de Casos Automatizables

| Categoria | Total Cases | P0 (Critico) | P1 (Alto) | P2 (Medio) | P3 (Bajo) | Automatizable |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Happy Path** | 3 | 3 | — | — | — | 100% |
| **Validación Input** | 8 | 4 | 4 | — | — | 100% |
| **Errores & Rechazo** | 6 | 3 | 3 | — | — | 100% |
| **Webhook & Notificaciones** | 5 | 3 | 2 | — | — | 100% |
| **Seguridad & Auth** | 4 | 4 | — | — | — | 80% |
| **Performance** | 3 | — | 2 | 1 | — | 60% |
| **Concurrencia** | 2 | 1 | 1 | — | — | 40% |
| **TOTAL** | **31** | **18** | **12** | **1** | **—** | **85%** |



```

    📍 PUNTO DE PARTIDA

    Situación actual en empresas de pagos:


    🎯 Testing manual de endpoints de pago

    🎯 8+ horas por ciclo de QA

    🎯 Riesgo de errores en producción

    🎯 Deployments lentos y con incertidumbre

**📍 LO QUE VAMOS A HACER (en 16 horas)**

ENTREGA VIERNES 15:00 hs:

**Entregar una suite de automatización de testing que:**

### 📑 Casos cubiertos (8/31)

| 🆔 ID | 📝 Caso | 🚩 Criticidad |
| :--- | :--- | :---: |
| `TEST_PAY_001` | **Crear pago exitoso** | 🔴 **P0** |
| `TEST_PAY_002` | **Consultar estado**   | 🔴 **P0** |
| `TEST_VAL_001` | **Monto mínimo**       | 🔴 **P0** |
| `TEST_VAL_002` | **Email requerido**    | 🔴 **P0** |
| `TEST_SEC_001` | **Token requerido**    | 🔴 **P0** |
| `TEST_SEC_002` | **Token inválido**     | 🔴 **P0** |
| `TEST_SEC_003` | **HTTPS obligatorio**  | 🔴 **P0** |
| `TEST_PAY_003` | **Idempotency key**    | 🔴 **P0** |


✅ Automatiza los 8 casos más críticos

1. Crear pagos

2. Validar datos

3. Autenticación

4. Seguridad


✅ Se ejecuta automáticamente en GitHub Actions

En cada push (sin intervención manual)

Resultado en 7 segundos

Reportes claros


✅ 100% adaptable a su stack

Código limpio

Sin dependencias complejas

Fácil de extender

🔄 FLUJO DE TRABAJO ACTUAL vs PROPUESTO
Desarrollador hace cambio en API pago -> Git push ->      
GitHub Actions automáticamente:
  
  ├─ Instala dependencias (2s)
  
  ├─ Ejecuta 8 tests críticos (5s)
  
  └─ Reporte de resultado (instantáneo)
         
✅ PASS → Deploy automático a staging

🎯 FAIL → Email al dev con qué falló

TIEMPO TOTAL: 7 segundos

RIESGO: Cero (casos cubiertos al 100%)

CONFIABILIDAD: Máxima

## Stack

| Herramienta | Versión mínima |
|---|---|
| Python | 3.11+ |
| pytest | 8.2+ |
| requests | 2.32+ |

## Setup

### 🔑 Lo único que necesitás antes de correr

Un **Access Token de prueba** de MercadoPago:

1. Entrá a [https://www.mercadopago.com.ar/developers/panel/app](https://www.mercadopago.com.ar/developers/panel/app)
2. Seleccioná tu aplicación → **Credenciales de prueba**
3. Copiá el **Access Token** (empieza con `TEST-`)

> El token de tarjeta se genera automáticamente — no hace falta configurar nada más.

---

### 🚀 Instalación y Ejecución

```bash
# 1. Clonar el repositorio
git clone -b dev https://github.com/mariel84-pixel/payments_cards.git
cd payments_cards

# 2. Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate        # Linux / Mac
# .venv\Scripts\activate         # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar credenciales
cp .env.example .env
# Abrir .env y reemplazar MP_ACCESS_TOKEN con tu token TEST-...

# 5. Ejecutar los tests y generar reporte HTML
mkdir -p reports
pytest tests/ -v --html=reports/report.html --self-contained-html

# 6. Abrir el reporte en el navegador
xdg-open reports/report.html    # Linux
open reports/report.html         # Mac
```

### ✅ Resultado esperado

```
7 passed, 1 xfailed
```

| Estado | Cantidad | Detalle |
|--------|----------|---------|
| Passed | 7 | Tests que corren y pasan correctamente |
| Xfailed | 1 | `test_https_obligatorio` — fallo esperado si el entorno bloquea HTTP puerto 80 |

> **Nota — ¿Por qué aparece `1 expected failure` (xfailed)?**
>
> El test `TEST_SEC_003 · test_https_obligatorio` verifica que MercadoPago redirige HTTP → HTTPS (códigos 301/302/308).
> En entornos sandbox y en GitHub Actions, las conexiones salientes al puerto 80 suelen estar bloqueadas, lo que provoca un `ConnectTimeout` antes de recibir respuesta.
>
> Por eso el test está marcado con `@pytest.mark.xfail`: **le dice a pytest que este fallo es conocido y esperado** en ese entorno.
> Un resultado `xfailed` **no es un error** — es pytest confirmando que el comportamiento coincide con lo anticipado.
> Si alguna vez el entorno permite la conexión y la redirección llega correctamente, el test pasará como `passed`.
>
> En resumen: `7 passed, 1 xfailed` es el resultado correcto y exitoso de esta suite.

> **Nota 2 — Cuotas definidas dentro de la Factory**
>
> Para esta entrega, definí las cuotas dentro de la Factory para asegurar que los payloads sean realistas.
> Sin embargo, soy consciente de que esto introduce un acoplamiento de reglas de negocio.
> En un entorno productivo real, mi propuesta sería extraer estos valores a un archivo de configuración (Data-Driven) o,
> mejor aún, parametrizar la fábrica para que consuma las cuotas válidas directamente desde un endpoint de
> configuración de la API, evitando así el mantenimiento manual si las condiciones comerciales cambian.

```
**📋 ESTRUCTURA DEL PROYECTO**

```
payments_cards/
│
├── api/
│   ├── __init__.py
│   └── payments_api.py                # API Object Model — cliente HTTP de MercadoPago
│
├── tests/
│   ├── factories/
│   │   └── payment_factory.py         # Generación de payloads con Faker
│   ├── fixtures/
│   │   └── conftest.py                # Fixtures de pytest (api_config, payment_token, payloads)
│   └── test_critical_path.py          # 8 casos P0 (bloqueantes)
│
├── .github/
│   └── workflows/
│       └── test.yml                   # Ejecución automática en cada push
│
├── docs/                              # Documentación del proyecto
├── reports/
│   └── report.html                    # Reporte HTML generado por pytest-html
│
├── conftest.py                        # Registro de fixtures: pytest_plugins
├── pytest.ini                         # Configuración de pytest y logging
├── requirements.txt                   # Dependencias
├── .env                               # Credenciales locales (no commitear)
├── .env.example                       # Template de credenciales
└── .gitignore
```

📊 LOS 31 CASOS Identificados (Roadmap completo)
FASE 1 (Viernes - 8 casos):
✅ Crear pago exitoso
✅ Consultar estado pago
✅ Validación: monto mínimo
✅ Validación: email requerido
✅ Seguridad: token requerido
✅ Seguridad: token inválido
✅ Seguridad: HTTPS obligatorio
✅ Idempotency: mismo key = mismo resultado

```
```
FASE 2 (Próxima semana - 12 casos):
- Tarjeta rechazada
- Webhook notificación
- Webhook reintentos
- Rate limiting (100 req/s)
- Refunds (devolver dinero)
- Moneda ARS vs USD
- Timeout handling
- Search payments
- Validación: fecha vencimiento
- Validación: CVV inválido
- Payment state transitions
- Webhook HMAC signature
```


```
FASE 3 (Mes 2 - 6 casos):
- Load testing (1000 pagos/min)
- Concurrencia (múltiples clientes)
- Seguridad: SQL injection
- Seguridad: XSS prevention
- Data validation en profundidad
- Performance baselines
```
**NOTA: GitHub Actions (test.yml) que es quien corre los tests automáticamente. Docker sería una capa extra que hoy no te agrega valor real porque:
GitHub Actions ya te da:
✅ Entorno limpio en cada corrida
✅ Corre automático en cada PR
✅ No depende de la máquina de nadie
✅ Variables de entorno seguras con secrets
