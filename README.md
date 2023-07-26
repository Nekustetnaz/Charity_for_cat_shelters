# Charity for cat shelters

## Description
This project helps cat shelters to collect and share donations.<br>
It uses a sqlite database and provides API access to services.<br>
The reports about fully invested projects could be sent to Google Sheets. 

## Run service:
To run the service, use the commands:
```
# Clone the repository and change directory:
git clone <github_link>
cd cat_charity_fund

# Create virtual environment:
python3 -m venv venv

# Activate virtual environment:
source venv/bin/activate  # for Linux/MacOS
source venv/scripts/activate  # for windows

# Install dependencies form the "requirements.txt" file:
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

The database is already created in file "fastapi.db"

Create ".env" file and fill it in according to the template:
```
# url to the database
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db

# your secret word for tokens
SECRET=

# information about your service account on Google Cloud Platform
TYPE=
PROJECT_ID=i
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=

# your email on Google Mail Service
EMAIL=
```

## Technologies
Python 3 <br>
FastAPI <br>
SQLAlchemy <br>

## The author of the project
Anton Akulov - https://github.com/Nekustetnaz
