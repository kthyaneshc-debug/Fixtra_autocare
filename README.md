# Fixtra AutoCare

A desktop-based **Car Service Management System** built with **Python, Tkinter and MySQL**. The application is designed to help an automobile service centre manage customers, vehicles, workshop jobs, inventory, billing and maintenance reminders in one place.

> **Project type:** Desktop application  
> **Primary stack:** Python · Tkinter · MySQL  
> **Status:** Academic / portfolio project

## Features

- **Dashboard** — service activity, business KPIs and recent operational insights
- **Customer Management** — maintain customer contact details
- **Vehicle Management** — register vehicles and associate them with customers
- **Service Jobs** — record complaints, diagnosis, priority and job status
- **Service Catalog** — maintain reusable service items and standard prices
- **Inventory** — track spare parts, quantities and reorder levels
- **Billing & Payments** — view job totals and payment status
- **Maintenance Reminders** — track upcoming service dates and odometer targets
- **MySQL Database** — relational tables for customers, vehicles, jobs, services, parts and payments

## Technology Stack

| Area | Technology |
|---|---|
| Language | Python |
| Desktop UI | Tkinter / ttk |
| Database | MySQL |
| Database driver | mysql-connector-python |
| Charts | Matplotlib |
| Configuration | python-dotenv |

## Project Structure

The application source is currently located in:

`NovaDrive_AutoCare/NovaDrive_AutoCare fixtra/`

Key files:

- `main.py` — application entry point
- `ui.py` — Tkinter screens and application workflow
- `database.py` — MySQL connection and query helpers
- `config.py` — environment-based application configuration
- `schema.sql` — database tables and starter service catalog
- `requirements.txt` — Python dependencies
- `.env.example` — example local database configuration

## Getting Started

### 1. Prerequisites

- Python 3.10 or newer
- MySQL Server
- Git (optional)

### 2. Open the application folder

Open a terminal in:

`NovaDrive_AutoCare/NovaDrive_AutoCare fixtra/`

### 3. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure MySQL credentials

Copy `.env.example` to a new file named `.env` and update the values for your local MySQL setup.

Never commit the real `.env` file or database credentials.

### 6. Run the application

Make sure MySQL Server is running, then execute:

```bash
python main.py
```

The application creates the configured database and required tables when it connects for the first time.

## Database

The default database name is `novadrive_autocare_db` to preserve compatibility with the existing project configuration. You can change it using the `DB_NAME` setting in your local `.env` file.

## Security Notes

- Keep credentials in a local `.env` file.
- Do not commit passwords, API keys or personal data.
- Use `.env.example` as a template only.
- Change any database password that was previously committed to version control.

## Future Improvements

- Role-based authentication and access control
- Search, filters and exportable reports
- Payment method selection and partial-payment handling
- Automated low-stock alerts
- Unit and integration tests
- Packaging the desktop application for Windows

## Author

**Thyanesh K**  
GitHub: [@kthyaneshc-debug](https://github.com/kthyaneshc-debug)

---

*Built as a practical portfolio project to demonstrate Python desktop development, SQL database design and business workflow automation.*
