# Playwright + Python Test Automation Framework

A production-ready test automation framework using Playwright, pytest, and Allure for reporting.

## Features

- ✅ **Parallel test execution** via pytest-xdist
- ✅ **Cross-browser support**: Chromium, Firefox, WebKit
- ✅ **Allure reporting** with screenshots on failure
- ✅ **Loguru logging** configured like log4j
- ✅ **Page Object Model** with base page class
- ✅ **Environment configuration** via .env
- ✅ **Automatic screenshots** on test failure

## Requirements

- Python 3.9+
- macOS / Linux / Windows
- Playwright browsers

## Installation

### Option 1: Virtual Environment (Recommended for Linux)

```bash
# Navigate to project directory
cd playwright-tests

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip to latest version
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### Option 2: macOS / Windows

```bash
# Navigate to project directory
cd playwright-tests

# Upgrade pip to latest version
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

> **Note for Linux:** If you get "externally-managed-environment" error, use Option 1 (virtual environment).

### Activate virtual environment

Every time you want to run tests:

```bash
source venv/bin/activate
```

## Configuration

All configuration is done via `.env` file:

```env
BASE_URL=https://example.com
BROWSER=chromium
HEADLESS=true
LOG_LEVEL=INFO
WORKERS=auto
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BASE_URL` | Base URL for tests | `https://example.com` |
| `BROWSER` | Browser to use | `chromium` |
| `HEADLESS` | Run in headless mode | `true` |
| `LOG_LEVEL` | Log level | `INFO` |
| `WORKERS` | Parallel workers | `auto` |

## Running Tests

### Run all tests in parallel (all browsers)

```bash
pytest -n auto --alluredir=reports/allure-results
```

### Run specific browser

```bash
# Chromium only
pytest --browser=chromium

# Firefox only
pytest --browser=firefox

# WebKit only
pytest --browser=webkit
```

### Run specific markers

```bash
# Run only smoke tests
pytest -m smoke

# Run only regression tests
pytest -m regression

# Run e2e tests
pytest -m e2e
```

### Run with specific number of workers

```bash
# Run with 4 parallel workers
pytest -n 4

# Run with auto-detected workers
pytest -n auto
```

### Rerun failed tests

```bash
# Rerun failed tests once
pytest --reruns 1
```

## Generating Allure Reports

### Serve report (local)

```bash
allure serve reports/allure-results
```

### Generate static report

```bash
allure generate reports/allure-results -o reports/allure-report --clean
```

### Open report in browser

```bash
allure open reports/allure-report
```

## Project Structure

```
playwright-tests/
├── .env                    # Environment configuration
├── pytest.ini              # Pytest configuration
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── conftest.py            # Pytest fixtures and hooks
├── pages/
│   └── base_page.py       # Base Page Object class
├── tests/
│   └── test_example.py    # Example tests
├── logs/                  # Test logs (auto-generated)
│   └── test_YYYY-MM-DD.log
└── reports/
    ├── allure-results/    # Allure test results
    └── allure-report/     # Generated Allure report
```

## Test Markers

| Marker | Description |
|--------|-------------|
| `smoke` | Quick smoke tests |
| `regression` | Full regression suite |
| `e2e` | End-to-end tests |
| `slow` | Tests that take longer |

## Logging

Logs are automatically generated with Loguru, configured similar to log4j:

- **Console**: Colored output with timestamp, level, and message
- **File**: Rotating logs at `logs/test_{date}.log`
- **Format**: `{time} | {level} | {name}:{line} - {message}`

## Allure Reporting Features

The framework automatically captures:

- 📸 **Screenshots on failure** - Attached to Allure report
- 📝 **Test steps** - Using `@allure.step` decorator
- 🌐 **Environment info** - Browser, platform, Python version
- 📊 **Test metadata** - Title, description, features, stories

### Using Allure Steps

```python
import allure
from pages.base_page import BasePage

@allure.step("Navigate to homepage")
def navigate_to_homepage(page):
    page.goto("https://example.com")

@allure.step("Fill login form")
def fill_login_form(page, username, password):
    page.fill("#username", username)
    page.fill("#password", password)
```

### Using Allure Attachments

```python
# Attach text
allure.attach(
    "Some text content",
    name="Custom Data",
    attachment_type=allure.attachment_type.TEXT,
)

# Attach HTML
allure.attach(
    "<h1>Hello</h1>",
    name="HTML",
    attachment_type=allure.attachment_type.HTML,
)
```

## Page Object Model

The framework includes a base `BasePage` class with common methods:

```python
from pages.base_page import BasePage

class MyPage(BasePage):
    def __init__(self, page, base_url):
        super().__init__(page, base_url)
    
    def navigate_to_section(self):
        return self.navigate("/section")

# Usage
def test_my_feature(page, base_url):
    my_page = MyPage(page, base_url)
    my_page.navigate_to_section()
    my_page.click("#button")
    my_page.assert_visible("#success-message")
```

### Available BasePage Methods

- `navigate(url)` - Navigate to URL
- `click(selector)` - Click element
- `fill(selector, value)` - Fill input
- `wait_for_element(selector)` - Wait for element
- `assert_visible(selector)` - Assert element is visible
- `assert_text_contains(selector, text)` - Assert text contains
- `take_screenshot(name)` - Take screenshot and attach to Allure

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Playwright Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install --with-deps chromium
      
      - name: Run tests
        run: pytest -n auto --alluredir=reports/allure-results
      
      - name: Upload Allure results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: allure-results
          path: reports/allure-results
```

## Troubleshooting

### Browser not installing

```bash
# Force reinstall browsers
playwright install --force

# Install specific browser
playwright install chromium
```

### Port already in use

If you get port errors, kill existing processes:

```bash
lsof -i :9222 | xargs kill -9
```

### Screenshot permission errors

Ensure the `reports` directory exists:

```bash
mkdir -p reports/allure-results
```

## License

MIT License
