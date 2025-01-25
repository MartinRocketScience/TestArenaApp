# Selenium Python Test Framework for TestArena

This repository contains automated tests for the TestArena application using Selenium WebDriver and Python.

## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose
- Git
- Chrome browser

## Setup Instructions

### 1. Docker Setup

1. Download TestArenaApp and extract it to your project directory:
   ```bash
   # Your project structure should look like this:
   selenium_python/
   ├── TestArenaApp/
   │   ├── docker-compose.yml
   │   └── ... (other TestArena files)
   ├── tests/
   ├── pages/
   └── ... (other project files)
   ```

2. Start Docker containers:
   ```bash
   cd TestArenaApp
   docker-compose up -d
   ```

3. Verify containers are running:
   ```bash
   docker ps
   ```

   You should see three containers:
   - docker-app
   - docker-phpmyadmin
   - docker-db

### 2. Python Environment Setup

1. Create and activate virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate # Linux/Mac
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy and configure environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file with your settings:
   ```
   BASE_URL=http://localhost
   BROWSER=chrome
   HEADLESS=False
   IMPLICIT_WAIT=10
   EXPLICIT_WAIT=20
   
   # Database configuration
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=root
   DB_NAME=testarena
   
   # Test user credentials
   TEST_USER_EMAIL=administrator@testarena.pl
   TEST_USER_PASSWORD=12qwAS
   ```

   > **⚠️ SECURITY WARNING**
   > 
   > The values shown above are just examples. Always:
   > - Set your own environment variables
   > - Never commit `.env` file to git repository
   > - Never share your credentials publicly
   > - Add `.env` to your `.gitignore` file
   > 
   > Exposing sensitive credentials can lead to security breaches!

## Project Structure

```
selenium_python/
├── pages/              # Page Object Models
│   ├── base_page.py
│   ├── login_page.py
│   ├── dashboard_page.py
│   └── ...
├── tests/              # Test files
│   ├── test_login.py
│   └── test_add_task.py
├── utils/              # Helper utilities
│   └── webdriver_helper.py
└── conftest.py         # Pytest configuration and fixtures
```

## Running Tests

### Running All Tests
```bash
pytest tests/ -v
```

### Running Specific Test File
```bash
pytest tests/test_login.py -v
```

### Running Specific Test Case
```bash
pytest tests/test_login.py -v -k "test_login_with_valid_credentials"
```

### Running Tests with Different Options
- With print statements: `pytest -v -s`
- With detailed output: `pytest -v --verbose`
- Generate HTML report: `pytest --html=report.html`

## Test Categories

1. Login Tests (`test_login.py`):
   - Valid credentials
   - Invalid credentials
   - Empty fields
   - Invalid email format

2. Task Management Tests (`test_add_task.py`):
   - Create new task
   - Task details verification

## Code Quality

The project uses several tools to maintain code quality:

### Linting and Style Checking
- `flake8`: Basic PEP-8 style checking
- `flake8-docstrings`: Docstring style checking
- `flake8-import-order`: Import order checking
- `flake8-quotes`: Quotation style checking
- `flake8-bugbear`: Additional bug checks

### Code Formatting
- `black`: Automatic code formatting
- `isort`: Import sorting

### Running Code Quality Tools

```bash
# Run flake8 checks
flake8 --exclude=venv,TestArenaApp,docker

# Format code with black
black .

# Sort imports with isort
isort .

# Check specific file or directory
flake8 pages/login_page.py
black pages/login_page.py
isort pages/login_page.py

# Show statistics
flake8 --statistics

# Show source code for each error
flake8 --show-source
```

### VS Code Integration

Add these settings to your `.vscode/settings.json` for real-time linting and formatting:

```json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": [
        "--config=.flake8"
    ],
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter"
    }
}
