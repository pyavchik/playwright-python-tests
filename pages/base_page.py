"""
Base Page Object class with common methods and Allure step decorators.
"""
import allure
from typing import Optional, Union, List
from loguru import logger
from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError


class BasePage:
    """
    Base Page Object class providing common methods for all page objects.
    Implements Page Object Model pattern with Allure integration.
    """
    
    def __init__(self, page: Page, base_url: str):
        """
        Initialize the base page.
        
        Args:
            page: Playwright Page instance
            base_url: Base URL of the application
        """
        self.page = page
        self.base_url = base_url
        self.logger = logger
    
    # =========================================================================
    # Navigation Methods
    # =========================================================================
    @allure.step("Navigate to {url}")
    def navigate(self, url: str) -> "BasePage":
        """
        Navigate to a specific URL.
        
        Args:
            url: URL to navigate to
            
        Returns:
            Self for chaining
        """
        full_url = f"{self.base_url}{url}" if not url.startswith("http") else url
        self.logger.info(f"Navigating to: {full_url}")
        self.page.goto(full_url, wait_until="domcontentloaded")
        self.logger.info(f"Successfully navigated to: {full_url}")
        return self
    
    @allure.step("Navigate to base URL")
    def navigate_to_base(self) -> "BasePage":
        """Navigate to the base URL."""
        return self.navigate(self.base_url)
    
    @allure.step("Go back")
    def go_back(self) -> "BasePage":
        """Navigate back in browser history."""
        self.logger.info("Navigating back")
        self.page.go_back()
        return self
    
    @allure.step("Go forward")
    def go_forward(self) -> "BasePage":
        """Navigate forward in browser history."""
        self.logger.info("Navigating forward")
        self.page.go_forward()
        return self
    
    @allure.step("Reload page")
    def reload(self) -> "BasePage":
        """Reload the current page."""
        self.logger.info("Reloading page")
        self.page.reload()
        return self
    
    # =========================================================================
    # Click Methods
    # =========================================================================
    @allure.step("Click element: {locator}")
    def click(
        self,
        locator: str,
        timeout: int = 30000,
        force: bool = False,
    ) -> "BasePage":
        """
        Click an element.
        
        Args:
            locator: Selector for the element
            timeout: Timeout in milliseconds
            force: Whether to force the click
            
        Returns:
            Self for chaining
        """
        self.logger.info(f"Clicking: {locator}")
        self.page.click(locator, timeout=timeout, force=force)
        self.logger.info(f"Clicked: {locator}")
        return self
    
    @allure.step("Double click element: {locator}")
    def double_click(self, locator: str, timeout: int = 30000) -> "BasePage":
        """Double click an element."""
        self.logger.info(f"Double clicking: {locator}")
        self.page.dblclick(locator, timeout=timeout)
        return self
    
    @allure.step("Right click element: {locator}")
    def right_click(self, locator: str, timeout: int = 30000) -> "BasePage":
        """Right click (context menu) an element."""
        self.logger.info(f"Right clicking: {locator}")
        self.page.click(locator, button="right", timeout=timeout)
        return self
    
    # =========================================================================
    # Input Methods
    # =========================================================================
    @allure.step("Fill input: {locator} with text")
    def fill(
        self,
        locator: str,
        value: str,
        clear_first: bool = True,
    ) -> "BasePage":
        """
        Fill an input field.
        
        Args:
            locator: Selector for the input
            value: Value to fill
            clear_first: Whether to clear the field first
            
        Returns:
            Self for chaining
        """
        self.logger.info(f"Filling '{locator}' with: {value}")
        if clear_first:
            self.page.fill(locator, "")
        self.page.fill(locator, value)
        self.logger.info(f"Filled '{locator}'")
        return self
    
    @allure.step("Type into: {locator}")
    def type_text(
        self,
        locator: str,
        text: str,
        delay: int = 50,
    ) -> "BasePage":
        """
        Type text character by character.
        
        Args:
            locator: Selector for the input
            text: Text to type
            delay: Delay between keystrokes in ms
            
        Returns:
            Self for chaining
        """
        self.logger.info(f"Typing into '{locator}': {text}")
        self.page.type(locator, text, delay=delay)
        return self
    
    @allure.step("Press key: {key}")
    def press_key(self, locator: str, key: str) -> "BasePage":
        """Press a key on an element."""
        self.logger.info(f"Pressing '{key}' on '{locator}'")
        self.page.press(locator, key)
        return self
    
    @allure.step("Clear input: {locator}")
    def clear(self, locator: str) -> "BasePage":
        """Clear an input field."""
        self.logger.info(f"Clearing: {locator}")
        self.page.fill(locator, "")
        return self
    
    # =========================================================================
    # Wait Methods
    # =========================================================================
    @allure.step("Wait for element: {locator}")
    def wait_for_element(
        self,
        locator: str,
        timeout: int = 30000,
        state: str = "visible",
    ) -> Locator:
        """
        Wait for an element to be in a specific state.
        
        Args:
            locator: Selector for the element
            timeout: Timeout in milliseconds
            state: Expected state (visible, hidden, attached, detached)
            
        Returns:
            Locator for the element
        """
        self.logger.info(f"Waiting for '{locator}' to be {state}")
        element = self.page.locator(locator).wait_for(timeout=timeout, state=state)
        self.logger.info(f"Element '{locator}' is now {state}")
        return element
    
    @allure.step("Wait for URL to contain: {pattern}")
    def wait_for_url_contains(self, pattern: str, timeout: int = 30000) -> "BasePage":
        """Wait for URL to contain a specific pattern."""
        self.logger.info(f"Waiting for URL to contain: {pattern}")
        self.page.wait_for_url(f"*{pattern}", timeout=timeout)
        return self
    
    @allure.step("Wait for navigation")
    def wait_for_load_state(self, state: str = "load") -> "BasePage":
        """Wait for a specific load state."""
        self.logger.info(f"Waiting for load state: {state}")
        self.page.wait_for_load_state(state)
        return self
    
    def wait_for_timeout(self, ms: int) -> "BasePage":
        """Wait for a specific amount of time."""
        self.page.wait_for_timeout(ms)
        return self
    
    # =========================================================================
    # Assertion Methods
    # =========================================================================
    @allure.step("Verify element is visible: {locator}")
    def assert_visible(self, locator: str, timeout: int = 30000) -> "BasePage":
        """Assert that an element is visible."""
        self.logger.info(f"Verifying '{locator}' is visible")
        self.page.locator(locator).is_visible(timeout=timeout)
        return self
    
    @allure.step("Verify element is hidden: {locator}")
    def assert_hidden(self, locator: str, timeout: int = 30000) -> "BasePage":
        """Assert that an element is hidden."""
        self.logger.info(f"Verifying '{locator}' is hidden")
        self.page.locator(locator).is_hidden(timeout=timeout)
        return self
    
    @allure.step("Verify element contains text: {locator}")
    def assert_text_contains(
        self,
        locator: str,
        expected_text: str,
        timeout: int = 30000,
    ) -> "BasePage":
        """Assert that an element contains specific text."""
        self.logger.info(f"Verifying '{locator}' contains: {expected_text}")
        element = self.page.locator(locator).first
        element.wait_for(timeout=timeout)
        actual_text = element.inner_text()
        assert expected_text in actual_text, (
            f"Expected '{expected_text}' in '{actual_text}'"
        )
        return self
    
    @allure.step("Verify URL contains: {pattern}")
    def assert_url_contains(self, pattern: str) -> "BasePage":
        """Assert that current URL contains a pattern."""
        self.logger.info(f"Verifying URL contains: {pattern}")
        assert pattern in self.page.url, f"URL '{self.page.url}' does not contain '{pattern}'"
        return self
    
    @allure.step("Verify page title contains: {title}")
    def assert_title_contains(self, title: str) -> "BasePage":
        """Assert that page title contains a string."""
        self.logger.info(f"Verifying title contains: {title}")
        page_title = self.page.title()
        assert title in page_title, f"Title '{page_title}' does not contain '{title}'"
        return self
    
    # =========================================================================
    # Screenshot Methods
    # =========================================================================
    @allure.step("Take screenshot")
    def take_screenshot(self, name: str = "screenshot") -> bytes:
        """
        Take a screenshot and attach to Allure.
        
        Args:
            name: Name for the screenshot
            
        Returns:
            Screenshot bytes
        """
        self.logger.info(f"Taking screenshot: {name}")
        screenshot = self.page.screenshot()
        
        allure.attach(
            screenshot,
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
        
        return screenshot
    
    # =========================================================================
    # Select/Dropdown Methods
    # =========================================================================
    @allure.step("Select option by value: {locator}")
    def select_option_by_value(
        self,
        locator: str,
        value: str,
    ) -> "BasePage":
        """Select an option from a dropdown by value."""
        self.logger.info(f"Selecting option with value '{value}' in '{locator}'")
        self.page.select_option(locator, value=value)
        return self
    
    @allure.step("Select option by label: {locator}")
    def select_option_by_label(
        self,
        locator: str,
        label: str,
    ) -> "BasePage":
        """Select an option from a dropdown by label."""
        self.logger.info(f"Selecting option with label '{label}' in '{locator}'")
        self.page.select_option(locator, label=label)
        return self
    
    # =========================================================================
    # JavaScript Execution
    # =========================================================================
    @allure.step("Execute JavaScript")
    def execute_script(self, script: str):
        """Execute JavaScript code."""
        self.logger.info(f"Executing JavaScript: {script[:50]}...")
        return self.page.evaluate(script)
    
    # =========================================================================
    # Get Methods
    # =========================================================================
    @allure.step("Get text from: {locator}")
    def get_text(self, locator: str) -> str:
        """Get text content from an element."""
        self.logger.info(f"Getting text from: {locator}")
        return self.page.locator(locator).inner_text()
    
    @allure.step("Get attribute: {locator}")
    def get_attribute(self, locator: str, attr: str) -> Optional[str]:
        """Get an attribute value from an element."""
        self.logger.info(f"Getting attribute '{attr}' from: {locator}")
        return self.page.locator(locator).get_attribute(attr)
    
    @allure.step("Get current URL")
    def get_current_url(self) -> str:
        """Get the current URL."""
        return self.page.url
    
    @allure.step("Get page title")
    def get_title(self) -> str:
        """Get the page title."""
        return self.page.title()
