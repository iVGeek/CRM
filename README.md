# GCS CRM System

A Customer Relationship Management system with proforma invoice generation, built for **GCS** (Global Commercial Services).

## Features

- **Client Management** – Create, view, edit, and delete clients with full contact details
- **Contact Management** – Track contacts linked to clients with name, email, phone, and position
- **Product Catalog** – Manage products/services with descriptions and unit pricing
- **Proforma Invoices** – Generate professional proforma invoices with:
  - Auto-generated invoice numbers (GCS-PI-YYYY-NNNN format)
  - Dynamic line items with quantity and pricing
  - Configurable tax rate (default 16%)
  - Status tracking (Draft, Sent, Accepted, Rejected, Expired)
  - PDF export with professional formatting
- **Dashboard** – Overview with summary stats and recent invoices

## Tech Stack

- Python / Flask
- SQLite (via Flask-SQLAlchemy)
- Bootstrap 5 (UI)
- WeasyPrint (PDF generation)

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Run tests
python -m pytest tests/ -v
```

The application runs at `http://localhost:5000` by default.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `gcs-crm-dev-secret-key` |
| `DATABASE_URL` | Database connection string | `sqlite:///crm.db` |
| `FLASK_DEBUG` | Enable debug mode | `false` |