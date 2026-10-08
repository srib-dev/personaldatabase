Setup:

1

# Mac: 

python -m venv .venv

# Linux:

## Fedora

*In terminal of this projects root folder*

Make sure you have uv installed:

`curl -LsSf https://astral.sh/uv/install.sh | sh`

Create the virtual environment:

`python3 -m venv .venv`

Activate the virtual environment:

`source .venv/bin/activate`

Install requirements:

`pip install -r requirements.txt`

Run the project locally:

`uv run fastapi dev`

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