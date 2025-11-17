# Mindsight - AI-Powered Personal Journal

A full-stack personal journaling application with AI-powered mood analysis and insights. Built with Flask and Google Gemini API, Mindsight helps you track your emotional journey and gain deeper self-awareness through intelligent reflections.

**Live Demo**: https://jubilantcapybara.pythonanywhere.com

**Video Demo**: https://youtu.be/MnddC-WRcwU

## Features

### Core Functionality
- Journal entries with timestamps
- AI mood classification using Google Gemini 2.5 Flash API
- AI reflections for each entry
- Entry management: view, browse, delete
- User authentication
- Multi-user support with private journals

### User Experience
- Modern, minimalist UI with gradient accents
- Light/Dark theme toggle
- Turquoise color scheme
- Responsive design for desktop and mobile
- Timezone-aware timestamps (automatic local conversion)
- Mood badges on entries
- Flash messages for user feedback

### Technical Features
- Secure password hashing (Werkzeug)
- SQLite database (file-based storage)
- Test suite (23 tests, 100% pass rate)
- RESTful routes
- Modular architecture with blueprints (auth, entries)

## Tech Stack

- **Backend**: Flask 3.0 (Python)
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Bootstrap 5.3
- **Icons**: Bootstrap Icons
- **AI**: Google Gemini 2.5 Flash API
- **Testing**: pytest
- **Deployment**: PythonAnywhere (web hosting)

## Prerequisites

- Python 3.10 or higher
- Google Gemini API key (free from [Google AI Studio](https://aistudio.google.com/apikey))
- pip (Python package manager)

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/AlgoBuild/mindsight.git
cd mindsight
```

### 2. Create virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```bash
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key-here
DATABASE=instance/mindsight.db
```

**To generate a secure SECRET_KEY:**
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Initialize the database

```bash
flask init-db
```

### 6. Run the application

```bash
flask run
```

Visit `http://127.0.0.1:5000` in your browser.

## Running Tests

```bash
# Run all tests
python -m pytest -v

```

All 23 tests should pass!

## Project Structure

```
mindsight/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── auth.py              # Authentication blueprint
│   ├── entries.py           # Journal entries blueprint
│   ├── db.py                # Database utilities
│   ├── gemini.py            # Gemini API integration
│   ├── schema.sql           # Database schema
│   ├── static/
│   │   └── images/          # Favicon and images
│   └── templates/
│       ├── base.html        # Base template with theme toggle
│       ├── index.html       # Landing page
│       ├── auth/            # Login/Register templates
│       └── entries/         # Journal entry templates
├── tests/                   # Test suite (23 tests)
├── instance/                # SQLite database (gitignored)
├── .env                     # Environment variables (gitignored)
├── .gitignore
├── requirements.txt
├── setup.py
└── README.md
```

## Usage

### First Time Setup
1. Register a new account
2. Log in with your credentials
3. Start journaling!

### Writing Entries
1. Click "**+ New Entry**" in the navbar
2. Write your thoughts in the text area
3. Click "**Save Entry**"
4. AI instantly analyzes your mood and provides reflection

### Managing Entries
- View all entries in "**My Entries**"
- Delete entries with confirmation modal
- Entries show:
  - Timestamp (in your local timezone)
  - Your journal text
  - AI-detected mood badge
  - AI reflection/insight

### Theme Toggle
- Click the **moon/sun icon** in navbar
- Theme preference saved in browser
- Works across all pages

## Security Features

- Password hashing with Werkzeug
- Session-based authentication
- User isolation (can only see own entries)
- Environment variables for secrets
- SQL injection prevention (parameterized queries)
- Login required decorator for protected routes

## AI Integration

The app uses **Google Gemini 2.5 Flash** for:
- **Mood Detection**: Analyzes emotional tone (happy, sad, anxious, etc.)
- **Reflections**: Generates personalized, supportive insights
- **Privacy Note**: Free tier stores data. Avoid sensitive personal information.

## Deployment (PythonAnywhere)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

Quick steps:
1. Push code to GitHub
2. Clone on PythonAnywhere
3. Set up virtual environment
4. Configure WSGI file
5. Set environment variables
6. Initialize database
7. Reload web app

## Troubleshooting

### Database errors
```bash
flask init-db
```

### Import errors
```bash
pip install -r requirements.txt
```

### Gemini API errors
- Check your API key in `.env`
- Verify quota at [Google AI Studio](https://aistudio.google.com/)
- Check internet connection

## CS50 Final Project

This is my final project for **CS50's Introduction to Computer Science** (2025).

**Project Requirements Met:**
- Web-based application
- Uses Python, Flask, SQL
- Integrates external API (Gemini)
- User authentication
- Comprehensive testing
- Clean, documented code
- README with setup instructions

## Future Improvements

Planned features for future versions:

- Change Password - Allow users to update their password
- Delete Account - Permanently remove account and all data
- Edit Entries - Modify past journal entries (complete CRUD)
- Export Data - Download journal entries as PDF or JSON
- Email Verification - Verify email addresses during registration
- Encryption at Rest - Encrypt journal entries in database for enhanced privacy


## Acknowledgments

- **CS50 Staff** - For an incredible course
- **Google** - For Gemini API access
- **Flask Community** - For excellent documentation
- **Bootstrap** - For UI components


## License

This project is open source and available under the MIT License.

## Author

**Nhi Mai**
- GitHub: [@AlgoBuild](https://github.com/AlgoBuild)

---

Made with love for CS50 Final Project 2025
