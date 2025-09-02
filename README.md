# OOTA

Online Order Tool Application

# Online Order Tool (OOTA)

A comprehensive Flask-based web application for managing pharmacy orders, integrating with multiple API endpoints, and handling database operations.

# Project Structure

OOTA/

- ├─ app.py # Flask app & routes (entrypoint)
- ├─ config.py # Environment & endpoint settings
- ├─ requirements.txt # Python dependencies
- ├─ templates/ # Jinja2 + Bootstrap pages
- ├─ JSON files/ # Saved request payloads (per client/payment/timestamp)
- ├─ .gitattributes
- └─ README.md

## Features

- **Order Management**: Create, update, and manage pharmacy orders
- **Product Management**: Add, edit, and remove products from orders
- **Payment Processing**: Support for multiple payment methods (Visa, Points, Tamara, Tabby, etc.)
- **API Integration**: Connect to multiple pharmacy API endpoints
- **Database Integration**: Query product information from SQL Server database
- **JSON Export**: Export order data in JSON format
- **Responsive UI**: Bootstrap-based responsive interface

## Supported Pharmacy Systems

- Adam Pharmacy (Production & Testing)
- UPC Pharmacy (Production & Testing)
- Whites Pharmacy (Production & Testing)

## Payment Methods

- Visa (visa, mastercard, mada, other)
- Points
- Tamara
- Tabby
- MisPay
- Emkan
- YouGotaGift
- OgMoney
- PostToCredit

## Installation

1. **Clone the repository**:
   ```bash
    git clone https://github.com/Hossam1104/OOTA.git
    cd OOTA
    python -m venv .venv
    . .venv/Scripts/activate # Windows
    # source .venv/bin/activate # macOS/Linux
    pip install -r requirements.txt

## Core flow

- Select Target System: Choose Adam / UPC / Whites (Prod/Test).

- Build Order: Add items (via product search/lookup), set quantities, delivery cost/flag, notes.
- Choose Payments: One or multiple from Visa/Points/BNPL/gift-wallets…
- Submit: App composes the final JSON and sends to the selected endpoint.
- Persist: The exact JSON is saved under JSON files/ (client + payment + timestamp for traceability). 


## Saving requests for audit
    {ClientName}_{PaymentMethod}_{YYYYMMDD-HHMMSS}.json

## Troubleshooting

| Symptom                           | Likely cause                      | Fix                                                                                    |
| --------------------------------- | --------------------------------- | -------------------------------------------------------------------------------------- |
| Product search 500                | SQL connection/driver mismatch    | Verify ODBC driver; test with `pyodbc.connect(...)` from REPL                          |
| “401/403” on submit               | Wrong API key / base URL          | Recheck tenant env vars; ensure prod vs test endpoints                                 |
| JSON saved but endpoint times out | Network/firewall or endpoint down | Add request timeout (e.g., 15s) & retry with backoff                                   |
| Arabic text garbled in JSON       | Encoding issue                    | Ensure UTF-8 everywhere and set proper `Content-Type: application/json; charset=utf-8` |

