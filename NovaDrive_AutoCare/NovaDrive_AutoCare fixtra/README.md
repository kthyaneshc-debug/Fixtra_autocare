# NovaDrive AutoCare
## Car Service Center Management & Automobile Maintenance Tracker

A practical desktop application built with **Python + Tkinter + MySQL** for real-world automobile service centers.

### Project highlights
- Attractive modern Tkinter dashboard
- Customer and vehicle management
- Supports all vehicle makes/models, including cars, EVs and hybrids
- Service job/work-order management
- Service history
- Maintenance reminders
- Inventory/parts tracking
- Billing and payment status
- Dashboard KPIs
- Searchable tables
- MySQL database with relational design
- Automatic database/table creation
- Sample service categories

### Supported examples
BMW, Mercedes-Benz, Audi, Toyota, Hyundai, Maruti Suzuki, Tata, Honda, Ford, Kia, Mahindra, Volkswagen, Nissan, Renault, BYD, Tesla, Volvo, Lexus, Skoda, Jeep, MG, plus any custom make/model.

## Setup

1. Install Python 3.10+.
2. Install MySQL Server and make sure it is running.
3. Open `config.py` and enter your MySQL username/password.
4. Install dependency:

```bash
pip install mysql-connector-python
```

5. Run:

```bash
python main.py
```

The application creates the database `novadrive_autocare_db` and required tables automatically.

## Default MySQL settings
- Host: localhost
- Port: 3306
- User: root
- Password: change_me

Change these in `config.py`.

## Folder structure

novadrive_autocare/
- main.py
- config.py
- database.py
- ui.py
- schema.sql
- requirements.txt
- README.md

## Real-world workflow
Customer -> Vehicle -> Service Job -> Inspection/Services -> Parts -> Invoice -> Payment -> Service History -> Next Service Reminder
