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

uv run fastapi dev