# Deploying Mindsight to PythonAnywhere

This guide walks you through deploying the Mindsight journal app to PythonAnywhere's free hosting tier.

## Prerequisites

- ✅ GitHub account with your code pushed
- ✅ PythonAnywhere free account
- ✅ Gemini API key
- ✅ Generated SECRET_KEY

## Step-by-Step Deployment

### 1. Create PythonAnywhere Account

1. Go to https://www.pythonanywhere.com/
2. Sign up for a **Beginner** (free) account
3. Verify your email

### 2. Open Bash Console

1. Log in to PythonAnywhere
2. Click **Consoles** tab
3. Start a new **Bash** console

### 3. Clone Your Repository

```bash
git clone https://github.com/YOUR_USERNAME/mindsight.git
cd mindsight
```

### 4. Create Virtual Environment

```bash
mkvirtualenv --python=/usr/bin/python3.10 mindsight-venv
```

This activates the virtual environment automatically.

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

Wait for all packages to install (may take 2-3 minutes).

### 6. Set Up Environment Variables

```bash
nano .env
```

Add these lines (replace with your actual values):

```bash
SECRET_KEY=your-generated-secret-key-here
GEMINI_API_KEY=your-gemini-api-key-here
FLASK_APP=app
```

**Save**: Press `Ctrl+O`, then `Enter`, then `Ctrl+X`

### 7. Initialize Database

```bash
export FLASK_APP=app
flask init-db
```

You should see: `Initialized the database.`

### 8. Configure Web App

#### 8.1 Create Web App

1. Go to **Web** tab
2. Click **Add a new web app**
3. Click **Next** (ignore domain name)
4. Select **Flask**
5. Select **Python 3.10**
6. Click **Next**

#### 8.2 Set Virtual Environment

1. Scroll to **Virtualenv** section
2. Enter path: `/home/YOUR_USERNAME/.virtualenvs/mindsight-venv`
3. Click checkmark

**Replace `YOUR_USERNAME`** with your actual PythonAnywhere username!

#### 8.3 Configure WSGI File

1. Click on **WSGI configuration file** link (under Code section)
2. **Delete everything** in the file
3. Paste this code (replace `YOUR_USERNAME`):

```python
import sys
import os

# Add your project directory to sys.path
project_home = '/home/YOUR_USERNAME/mindsight'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables
from dotenv import load_dotenv
project_folder = os.path.expanduser(project_home)
load_dotenv(os.path.join(project_folder, '.env'))

# Import Flask app
from app import create_app
application = create_app()
```

4. Click **Save** (top right)

#### 8.4 Configure Static Files

1. Go back to **Web** tab
2. Scroll to **Static files** section
3. Click **Enter URL** and enter: `/static/`
4. Click **Enter path** and enter: `/home/YOUR_USERNAME/mindsight/app/static/`
5. Click checkmark ✓

### 9. Reload Web App

1. Scroll to top of **Web** tab
2. Click green **Reload YOUR_USERNAME.pythonanywhere.com** button
3. Wait for reload to complete

### 10. Test Your App

Visit: `https://YOUR_USERNAME.pythonanywhere.com`

You should see your Mindsight landing page! 🎉

## Troubleshooting

### Error: "Something went wrong"

**Check error log**:
1. Go to **Web** tab
2. Click **Error log** link
3. Look for the most recent error

**Common issues**:

#### Import errors:
```bash
cd ~/mindsight
workon mindsight-venv
pip install -r requirements.txt
```

#### Database not found:
```bash
cd ~/mindsight
export FLASK_APP=app
flask init-db
```

#### Wrong virtualenv path:
Make sure `/home/YOUR_USERNAME/.virtualenvs/mindsight-venv` uses YOUR actual username.

#### WSGI file errors:
Double-check you replaced `YOUR_USERNAME` in the WSGI configuration.

### App works but static files missing

1. Check **Static files** mapping in Web tab
2. Verify path: `/home/YOUR_USERNAME/mindsight/app/static/`
3. Make sure favicon exists in `app/static/images/`

### Environment variables not working

```bash
cd ~/mindsight
cat .env  # Check if file exists and has correct values
```

## Updating Your App

When you make changes to your code:

```bash
# In PythonAnywhere Bash console
cd ~/mindsight
git pull origin main

# If requirements.txt changed:
workon mindsight-venv
pip install -r requirements.txt

# If database schema changed:
export FLASK_APP=app
flask init-db

# Then reload web app in Web tab
```

## Free Tier Limitations

PythonAnywhere free accounts have:
- 512MB disk space
- One web app at `your-username.pythonanywhere.com`
- 100s CPU-seconds per day (CPU-seconds measure how long your code uses full processor power, and while hitting 100% only slows processes slightly, typical programs rarely need much since they often wait on input/output.)
- Restricted outbound Internet access from your apps
- No IPython/Jupyter notebook suppor



## Security Notes

- ✅ Never commit `.env` file to GitHub
- ✅ Use strong SECRET_KEY (64+ characters)
- ✅ Regenerate API keys if exposed
- ✅ Use environment variables for all secrets

## Need Help?

- PythonAnywhere Forums: https://www.pythonanywhere.com/forums/
- PythonAnywhere Help: https://help.pythonanywhere.com/
- Flask Documentation: https://flask.palletsprojects.com/

---

