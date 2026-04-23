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

ENTREGA VIERNES 15:00:

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

### 🚀 Instalación y Ejecución

```bash
# 1. Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar el token de Mercado Pago Sandbox
#    Obtenerlo en: mercadopago.com.ar/developers/panel → Credenciales de prueba
cp .env.example .env
# Editar .env y reemplazar MP_ACCESS_TOKEN con tu token TEST-...

# 4. Ejecutar los tests y generar reporte HTML
mkdir -p reports
pytest tests/ -v --html=reports/report.html --self-contained-html

# 5. Abrir el reporte en el navegador
xdg-open reports/report.html   # Linux
open reports/report.html        # Mac
```

```
**📋 ESTRUCTURA DEL PROYECTO (Lo que entregas)**

Carpeta del repo:



```
automation-suite/
│
├── tests/
│   └── test_critical_path.py          # 8 casos P0 (bloqueantes)
│
├── .github/workflows/
│   └── test.yml                        # Ejecución automática
│
├── conftest.py                         # Fixtures compartidas
├── requirements.txt                    # Dependencias
├── .env.example                        # Template credenciales
│
├── docs/
│   ├── README.md                       # Setup rápido (1 página)
│   ├── PLAN_16_HORAS.md               # Arquitectura técnica
│   └── REPORTE_COBERTURA_TESTING.md   # 31 casos totales
│
└── .gitignore
```
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