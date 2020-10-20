# Classification Engine for Monetory Transactions (Expense Manager)

**You can check the demo of this application at: https://expensemanager.xyz**

## Prerequisites:

- You must have **python** and **pip** installed in your system (v2.6+).
- To install the latest version of python - https://www.python.org/downloads/
- To install the latest version of pip - https://pip.pypa.io/en/stable/installing/

## Clone the repository

- Clone the project
`git clone https://github.com/ramkrishnan6/expenseManager.git`

## Install necessary packages

- `cd expenseManager`
- `pip install -r requirements.txt`

## Run Django's Development server

`python manage.py runserver`

## Available endpoints:
- /
- /login
- /register
- /dashboard
- /manual
- /bill
- /csv
- /transactions
- /charts
- /budget
- /analysis
- /profile
- /reset-password

## Important NOTE:
- Make a `config.py` file in the root directory and initialize the following 
```
SECRET_KEY = "<secret key>"
ALLOWED_HOSTS = "<allowed hosts>"
EMAIL_HOST_USER = "< your_email_id>"
EMAIL_HOST_PASSWORD = "<your_password>"
```

- There are some endpoints that does not accept GET requests, hence not listed here.<br/>
You can find the complete URL mapping at `expenseManager/myapp/urls.py`
