# Charity for cat shelters

### Description
This project helps cat shelters to collect and share donations collecting donations for various targeted projects <br>
Several target projects can be opened at the same time. Each project has a name, description and an amount that is planned to be collected. After the required amount is collected, the project is closed. <br>
Donations to projects are received according to the first in first out principle: all donations go to the project opened earlier than others. When this project collects the necessary amount and closes, donations begin to flow to the next project.
Reports about fully invested projects could be sent to Google Sheets. 

### User roles and access permissions
- Guest (not authenticated user) — can view a list of all projects;
- Authenticated user — can view a list of all projects and add donations. This role is assigned by default to each new user;
- Supepuser — can create and view projects, delete projects without donations, update name and description of an existing project. Set a new required amount for a project (but not less than an amount already contributed);
No one is allowed to update an amount of deposited donations via the API, delete or modify closed projects, change the dates of creation and closure of projects.

### API services
- Auth: sign up, sign in, logout;
- Users: get user, update user;
- Charity_projects: get, create, update, delete charity projects;
- Donations: get, create donations;
- Google: create a report in Google spreadsheets with closed projects. 

### Run service:
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

### Technologies
Python 3 <br>
FastAPI <br>
SQLAlchemy <br>
Alembic

### Author
Anton Akulov - https://github.com/Nekustetnaz
