# Mindsight

AI-powered personal journaling with mood analysis and reflections. Built with Flask and Gemini API.

Live Demo: https://jubilantcapybara.pythonanywhere.com

Video Demo: https://youtu.be/MnddC-WRcwU

## Features

- Write and save journal entries
- Automatic mood classification (Google Gemini 2.5 Flash)
- AI-generated reflections for each entry
- View and delete entries
- User registration and login (per-user private journals)
- Responsive UI with light/dark theme

## Tech Stack

- Backend: Flask (Python)
- Database: SQLite
- Frontend: HTML, CSS, Bootstrap 5
- AI: Google Gemini 2.5 Flash API
- Testing: pytest
- Deployment: PythonAnywhere

## Prerequisites

- Python 3.10+
- Google Gemini API key (https://aistudio.google.com/apikey)

## Quick Start

1) Clone the repository

```bash
git clone https://github.com/AlgoBuild/mindsight.git
cd mindsight
```

2) Create and activate a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

3) Install dependencies

```bash
pip install -r requirements.txt
```

4) Configure environment

Create a .env file in the project root:

```bash
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key
GEMINI_API_KEY=your-gemini-api-key
DATABASE=instance/mindsight.db
```

Generate a secure SECRET_KEY (optional):

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

5) Initialize the database

```bash
flask init-db
```

6) Run the app

```bash
flask run
```

Open http://127.0.0.1:5000

## Tests

```bash
python -m pytest -v
```


## License

MIT License

## Author

Nhi Mai — GitHub: https://github.com/AlgoBuild
