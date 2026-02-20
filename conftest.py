"""
Pytest configuration with Playwright fixtures and Allure integration.
"""
import os
import allure
import pytest
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, Playwright

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = os.getenv("BASE_URL", "https://example.com")
BROWSER = os.getenv("BROWSER", "chromium").lower()
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
WORKERS = os.getenv("WORKERS", "auto")

# Paths
PROJECT_ROOT = Path(__file__).parent
LOGS_DIR = PROJECT_ROOT / "logs"
ALLURE_RESULTS_DIR = PROJECT_ROOT / "reports" / "allure-results"

# Ensure directories exist
LOGS_DIR.mkdir(parents=True, exist_ok=True)
ALLURE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ==============================================================================
# Loguru Configuration (like log4j)
# ==============================================================================
def setup_loguru():
    """Configure loguru similar to log4j."""
    # Remove default logger
    logger.remove()
    
    # Console output with colors
    logger.add(
        lambda msg: print(msg, end=""),
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=LOG_LEVEL,
        colorize=True,
    )
    
    # File rotation (logs/test_{date}.log)
    log_file = LOGS_DIR / f"test_{datetime.now().strftime('%Y-%m-%d')}.log"
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} - {message}",
        level=LOG_LEVEL,
        rotation="00:00",  # New file at midnight
        retention="30 days",  # Keep for 30 days
        compression="zip",  # Compress old logs
        encoding="utf-8",
    )
    
    return logger


# Setup logging on module import
test_logger = setup_loguru()


# ==============================================================================
# Pytest Configuration Hooks
# ==============================================================================
def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "regression: Full regression suite")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Tests that take longer to run")


def pytest_runtest_makereport(item, call):
    """Hook to capture screenshot on test failure."""
    if call.when == "call":
        if call.excinfo is not None:
            # Get the page fixture from the test
            page = item.funcargs.get("page")
            if page:
                try:
                    # Take screenshot
                    screenshot_bytes = page.screenshot()
                    
                    # Attach to Allure
                    allure.attach(
                        screenshot_bytes,
                        name="screenshot_on_failure",
                        attachment_type=allure.attachment_type.PNG,
                    )
                    
                    test_logger.error(f"Screenshot captured on failure: {item.name}")
                except Exception as e:
                    test_logger.error(f"Failed to capture screenshot: {e}")


# ==============================================================================
# Playwright Fixtures
# ==============================================================================
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Configure browser launch arguments."""
    return {
        **browser_type_launch_args,
        "headless": HEADLESS,
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
            "--no-sandbox",
        ],
    }


@pytest.fixture(scope="session")
def browser_type(browser_type):
    """Return the browser type based on configuration."""
    return browser_type


@pytest.fixture(scope="function")
def browser_context(
    browser_type: Browser,
    browser_context_args,
    playwright: Playwright,
) -> BrowserContext:
    """Create a browser context with custom options."""
    context = browser_type.new_context(
        **browser_context_args,
        viewport={"width": 1920, "height": 1080},
        locale="en-US",
        timezone_id="Europe/Kiev",
    )
    
    # Add console log listener for debugging
    def handle_console(msg):
        if msg.type == "error":
            test_logger.error(f"Browser console error: {msg.text}")
    
    context.on("console", handle_console)
    
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(browser_context: BrowserContext) -> Page:
    """Create a new page for each test."""
    page = browser_context.new_page()
    
    # Add page error handler
    def handle_page_error(error):
        test_logger.error(f"Page error: {error}")
    
    page.on("pageerror", handle_page_error)
    
    yield page
    page.close()


@pytest.fixture(scope="session")
def base_url() -> str:
    """Return the base URL from configuration."""
    return BASE_URL


@pytest.fixture(scope="session")
def config() -> dict:
    """Return the full configuration dictionary."""
    return {
        "base_url": BASE_URL,
        "browser": BROWSER,
        "headless": HEADLESS,
        "log_level": LOG_LEVEL,
        "workers": WORKERS,
    }


# ==============================================================================
# Allure Environment Info
# ==============================================================================
@pytest.fixture(scope="session", autouse=True)
def add_allure_environment_info(browser_type):
    """Add environment information to Allure report."""
    try:
        # Try newer allure-pytest API
        allure.dynamic.env("Platform", "macOS")
        allure.dynamic.env("Browser", browser_type.name.capitalize())
        allure.dynamic.env("Headless", str(HEADLESS))
        allure.dynamic.env("Base_URL", BASE_URL)
        allure.dynamic.env("PythonVersion", os.sys.version.split()[0])
    except AttributeError:
        # Fallback: skip if not available (older versions)
        pass
