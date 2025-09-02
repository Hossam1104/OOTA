# OOTA — Online Order Tool Application

A lightweight **Flask** web app to compose and submit **online pharmacy orders** across multiple backends, with fast product lookup from **SQL Server**, flexible **multi‑payment** handling, and **JSON export** for traceability.

> This README is tailored to the current repository layout (`app.py`, `config.py`, `templates/`, and `JSON files/`). Adjust any environment variable names to match your `config.py` if they differ.

---

## ✨ Features

- **Order builder**: Add/edit items, delivery flags & cost, notes, discounts.
- **Multi‑payment support**: Split or single payments.
- **Product lookup**: Query SQL Server for items (e.g., by barcode/material).
- **Tenant endpoints**: Target different systems (Prod/Test) from one UI.
- **JSON export**: Persist every successful request under `JSON files/` with timestamped names.
- **Responsive UI**: Bootstrap/Jinja templates under `/templates`.

### Supported pharmacy systems (as configured in the repo)
- **Adam Pharmacy** (Production & Testing)
- **UPC Pharmacy** (Production & Testing)
- **Whites Pharmacy** (Production & Testing)

### Payment methods (as currently documented)
- Visa (visa, mastercard, mada, other)
- Points
- Tamara
- Tabby
- MisPay
- Emkan
- YouGotaGift
- OgMoney
- PostToCredit

---

## 🗂️ Repository structure

```
OOTA/
├─ app.py                 # Flask app & routes (entry point)
├─ config.py              # Environment & endpoint settings
├─ requirements.txt       # Python dependencies
├─ templates/             # Jinja2 + Bootstrap pages
├─ JSON files/            # Saved request payloads (client+payment+timestamp)
├─ .gitattributes
└─ README.md
```

---

## 🚀 Quick start

### 1) Prerequisites
- Python **3.10+** (3.11 recommended)
- **SQL Server** accessible from your machine (read‑only is fine for lookups)
- API base URLs/keys for your target systems (Prod/Test)

### 2) Setup

```bash
git clone https://github.com/Hossam1104/OOTA.git
cd OOTA

python -m venv .venv
# Windows
. .venv/Scripts/activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
```

> Dependencies are pinned in `requirements.txt`. If you meet driver issues for SQL Server, install a suitable ODBC driver and `pyodbc`/`pymssql` as needed.

### 3) Configure

You can configure **either** in `config.py` **or** via environment variables that `config.py` reads. Suggested keys (rename to match your file if different):

| Key | Purpose |
|---|---|
| `FLASK_ENV` | `development` / `production` |
| `SECRET_KEY` | Flask session secret |
| `SQLSERVER_HOST`, `SQLSERVER_DB`, `SQLSERVER_USER`, `SQLSERVER_PASSWORD` | Product lookup connection |
| `ADAM_API_BASE`, `UPC_API_BASE`, `WHITES_API_BASE` | Tenant base URLs (Prod/Test) |
| `*_API_KEY` / `*_AUTH` | Auth tokens/keys if required |
| `SAVE_JSON_DIR` | Defaults to `JSON files/` |

**.env example** (optional, if you choose to load env vars):
```dotenv
FLASK_ENV=development
SECRET_KEY=change-me

SQLSERVER_HOST= .
SQLSERVER_DB= RmsCashierSrv
SQLSERVER_USER= sa
SQLSERVER_PASSWORD= P@ssw0rd

ADAM_API_BASE=https://api.adam.example/v1
UPC_API_BASE=https://api.upc.example/v1
WHITES_API_BASE=https://api.whites.example/v1

SAVE_JSON_DIR=JSON files
```

### 4) Run locally

```bash
# Dev
set FLASK_ENV=development   # PowerShell: $env:FLASK_ENV='development'
python app.py               # app listens on http://127.0.0.1:5000
```

For production, see **Deployment** below.

---

## 🧩 How it works

1) **Select tenant** (Adam/UPC/Whites; Prod/Test).
2) **Build order**: add items (via lookup), set qty, delivery cost/flag, notes.
3) **Choose payment(s)**: card, points, BNPL, wallets, etc.
4) **Submit**: the app composes final JSON and posts to the tenant endpoint.
5) **Persist**: on success, the exact payload is saved to `JSON files/` using:
   ```
   {ClientName}_{PaymentMethod}_{YYYYMMDD-HHMMSS}.json
   ```
   Example: `UPC_Visa_20250902-143012.json`

### Product lookup (SQL Server)
- A Flask route queries your SQL Server for product attributes (name, price, tax code, UOM, etc.) based on barcode/material.
- Use a **read‑only** SQL login for this purpose.

### Key routes (typical)
> Names may vary—see `app.py` for the exact list.
- `GET /` — Home (order builder)
- `POST /orders/preview` — Validate/preview the outgoing JSON (no submit)
- `POST /orders/submit` — Submit to the selected tenant and save JSON
- `GET /products/search?query=...` — Item lookup returning JSON for the UI
- `GET /health` — Simple health probe

---

## ✅ Validation & error handling (recommended checks)

- **Totals**: sum(payments) == grand total; no negative quantities/prices.
- **Delivery**: enforce `is_delivery` + `order_delivery_cost` logic.
- **Tenant rules**: per‑tenant adapters for field/enum differences.
- **Timeouts/retries**: HTTP timeouts with exponential backoff.
- **Encoding**: UTF‑8 JSON; `Content-Type: application/json; charset=utf-8`.

---

## 🧪 Testing

We recommend a small test suite to protect critical logic:

```
tests/
  test_json_shape.py         # required fields, types, totals
  test_payments_validation.py# split payments, rounding, edge cases
  test_endpoint_adapters.py  # per‑tenant transforms
```

Run with:
```bash
pip install -r requirements.txt
pip install pytest
pytest -q
```

---

## ☁️ Deployment

**Linux (Gunicorn + Nginx)**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
# Nginx proxies :80 -> 127.0.0.1:8000
```

**Windows (Waitress)**
```bash
pip install waitress
waitress-serve --port=8000 app:app
```

Set `FLASK_ENV=production`, real SQL creds, and production endpoints. Configure log rotation for access logs and the `JSON files/` archive.

---

## 🔐 Security

- **Secrets**: never commit API keys—use env vars or a secrets manager.
- **PII**: avoid saving customer PII to `JSON files/`; mask if required.
- **TLS**: call tenant APIs over HTTPS and verify certificates.
- **Least privilege**: use read‑only SQL logins for lookups.

---

## 🧭 Roadmap (suggested)

- **Per‑tenant adapters** for field normalization and validations.
- **Preset orders** / **duplicate from previous** to speed QA workflows.
- Optional **XML export** in addition to JSON (toggle).
- **User accounts** / roles (per‑tenant permissions).
- Basic **webhooks** for status callbacks where supported.

---

## 🙌 Credits

Built with **Flask** + **Jinja2/Bootstrap**. HTML templates live in `/templates`; Python entry point is `app.py`; saved payloads go to `JSON files/`.

---

## 📝 License

> No license file is currently included. If you intend to open‑source, add `LICENSE` (e.g., MIT). Otherwise, treat this repository as **proprietary** within your organization.
