"""
Example test demonstrating Playwright + pytest + Allure integration.
This test runs across multiple browsers and uses Allure for reporting.
"""
import pytest
import allure
from faker import Faker
from pages.base_page import BasePage


# Initialize Faker for generating test data
fake = Faker()


@allure.feature("Example Tests")
@allure.story("Playwright Integration")
class TestExample:
    """Example test class demonstrating the framework features."""
    
    @pytest.mark.smoke
    @pytest.mark.e2e
    @allure.title("Test page navigation")
    @allure.description("Verify that navigation to the base URL works correctly")
    def test_page_navigation(
        self,
        page,
        base_url,
    ):
        """
        Test basic page navigation.
        Demonstrates: Navigation, logging, Allure steps.
        """
        base_page = BasePage(page, base_url)
        
        with allure.step("Navigate to example.com"):
            base_page.navigate("https://example.com")
        
        with allure.step("Verify page title"):
            base_page.assert_title_contains("Example")
        
        with allure.step("Take screenshot of loaded page"):
            base_page.take_screenshot("example_homepage")
        
        # Verify URL
        assert "example.com" in base_page.get_current_url()
    
    @pytest.mark.smoke
    @pytest.mark.e2e
    @allure.title("Test element interaction")
    @allure.description("Verify that we can interact with page elements")
    def test_element_interaction(
        self,
        page,
        base_url,
    ):
        """
        Test element interaction (navigation, clicking, text verification).
        Demonstrates: Click, fill, assert, steps.
        """
        base_page = BasePage(page, base_url)
        
        # Navigate to example.com
        base_page.navigate("https://example.com")
        
        # Click on the "More information" link (linking to iana.org)
        with allure.step("Click on 'More information' link"):
            base_page.click("text=More information")
        
        # Wait for navigation
        base_page.wait_for_url_contains("iana.org", timeout=10000)
        
        # Verify we're on iana.org
        base_page.assert_url_contains("iana.org")
        
        # Take screenshot
        base_page.take_screenshot("iana_page")
    
    @pytest.mark.regression
    @allure.title("Test form interaction with Faker data")
    @allure.description("Demonstrates using Faker to generate test data")
    @pytest.mark.skip(reason="Example only - example.com doesn't have a form")
    def test_form_with_faker_data(
        self,
        page,
        base_url,
    ):
        """
        Test form filling with dynamically generated data.
        Demonstrates: Faker integration, form filling.
        """
        base_page = BasePage(page, base_url)
        
        # Generate fake data
        name = fake.name()
        email = fake.email()
        message = fake.text(max_nb_chars=100)
        
        with allure.step("Generate test data"):
            allure.attach(
                f"Name: {name}\nEmail: {email}\nMessage: {message}",
                name="Test Data",
                attachment_type=allure.attachment_type.TEXT,
            )
        
        # Navigate to form
        base_page.navigate("/contact")
        
        # Fill form
        with allure.step("Fill contact form"):
            base_page.fill("#name", name)
            base_page.fill("#email", email)
            base_page.fill("#message", message)
        
        # Submit
        base_page.click("#submit")
        
        # Verify success
        base_page.assert_visible(".success-message")
        
        # Take screenshot
        base_page.take_screenshot("form_submitted")
    
    @pytest.mark.regression
    @allure.title("Test page content verification")
    @allure.description("Verify page content and elements")
    def test_page_content_verification(
        self,
        page,
        base_url,
    ):
        """
        Test content verification on a page.
        Demonstrates: Text verification, multiple assertions.
        """
        base_page = BasePage(page, base_url)
        
        # Navigate to example.com
        base_page.navigate("https://example.com")
        
        # Verify main heading
        with allure.step("Verify main heading contains 'Example'"):
            base_page.assert_text_contains("h1", "Example Domain")
        
        # Verify paragraph text
        with allure.step("Verify introduction text"):
            base_page.assert_text_contains(
                "body > div > p:nth-child(3)",
                "example domain"
            )
        
        # Verify link exists
        with allure.step("Verify 'Learn more' link exists"):
            base_page.assert_visible("text=Learn more")
        
        # Take final screenshot
        base_page.take_screenshot("content_verified")


@allure.feature("Example Tests")
@allure.story("Parallel Execution")
class TestParallel:
    """Tests designed to run in parallel safely."""
    
    @pytest.mark.smoke
    @allure.title("Test parallel execution - simple")
    @pytest.mark.parametrize("page_param", ["value1", "value2", "value3"], indirect=True)
    def test_parallel_simple(
        self,
        page,
        base_url,
        page_param,
    ):
        """
        Simple parallel test to verify pytest-xdist works.
        Each worker gets its own browser context.
        """
        base_page = BasePage(page, base_url)
        
        base_page.navigate("https://example.com")
        base_page.take_screenshot(f"parallel_test_{page_param}")
        
        # Unique assertion per parameter
        assert base_page.get_title() == "Example Domain"
    
    @pytest.mark.smoke
    @allure.title("Test with unique browser context per test")
    def test_unique_context(
        self,
        page,
        base_url,
    ):
        """
        Test that each test gets a unique browser context.
        This is handled automatically by the fixture.
        """
        base_page = BasePage(page, base_url)
        
        # Each test gets a fresh page
        base_page.navigate("https://example.com")
        
        # Verify isolation by checking page URL
        assert base_page.get_current_url() == "https://www.example.com/"
