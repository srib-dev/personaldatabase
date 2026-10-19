Setup:

1

# Mac / Linux:
python3 -m venv .venv

# Windows:
python -m venv .venv

2

# Mac / Linux:
source .venv/bin/activate

# Windows (PowerShell):
.venv\Scripts\Activate.ps1

3

pip install -r requirements.txt

4

# Opprett .env i rotmappen:
SECRET_KEY=din-hemmelige-nokkel
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
ADMIN_EMAIL=admin@srib.no
ADMIN_PASSWORD=Passord123

5

uv run fastapi dev