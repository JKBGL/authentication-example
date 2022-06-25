## Simple Authentication Example
This small project is the aftermath of an 8 hour speed coding session, and it's code is complete ass but I love it.

---

## Screenshots
- Main page (Desktop)
[image mini-application]

- Dashboard (Desktop)
[image mini-application-dashboard]

- Main page (Mobile)
[image mini-application-mobile]

- Dashboard (Mobile)
[image mini-application-dashboard-mobile]

---

## Installation

### Cloning
```bash
> git clone https://github.com/JKBGL/auth-example
> cd auth-example
```

### Requirements
- Python 3.10+
- MySQL 8

### Installing python packages
```bash
# Install required python packages
> py -3.10 -m pip install -r requirements.txt
```

### Setting up MySQL
Note: You need to have an existing database for this.
```bash
# Initialize the application's required table
> mysql -u database_user -p database_name < setup/db.sql
```

### Configuration
```bash
# Copy configuration file and open for editing
> cp setup/.env.sample .env
> nano .env
```

### Running
There are two ways of running this application:
```bash
# 1. Using `main.py`
> py -3.10 ./main.py

# 2. Or using uvicorn directly:
> py -3.10 -m uvicorn main:app --reload --no-server-header --no-date-header
```

---

License : `Mozilla Public License 2.0`
Author : Jakatebel
