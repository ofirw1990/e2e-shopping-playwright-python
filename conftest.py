"""
Pytest Configuration - הגדרות גלובליות
"""
import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
import yaml
import os


def pytest_configure(config):
    """הגדרות כלליות לפני ריצת הטסטים"""
    # יצירת תיקיות
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("allure-results", exist_ok=True)


@pytest.fixture(scope="session")
def config():
    """קריאת קובץ הקונפיגורציה"""
    config_path = "config/test_config.yaml"
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


@pytest.fixture(scope="session")
def browser_type_launch_args(config):
    """הגדרות לדפדפן"""
    return {
        "headless": config["browser"]["headless"],
        "slow_mo": config["browser"]["slow_mo"],
    }


@pytest.fixture(scope="session")
def browser_context_args(config):
    """הגדרות לקונטקסט הדפדפן"""
    return {
        "viewport": {"width": 1920, "height": 1080},
        "locale": "en-US",
        "timezone_id": "America/New_York",
    }


@pytest.fixture(scope="function")
def page(browser: Browser, context: BrowserContext) -> Page:
    """
    פיקצ'ר לדף - נוצר לכל טסט
    הדפדפן נשאר פתוח בין הטסטים
    """
    page = context.new_page()
    page.set_default_timeout(30000)
    
    yield page
    
    # ניקוי אחרי הטסט
    page.close()


@pytest.fixture(scope="session")
def context(browser: Browser, browser_context_args):
    """קונטקסט דפדפן - משותף לכל הטסטים בסשן"""
    context = browser.new_context(**browser_context_args)
    
    yield context
    
    context.close()


@pytest.fixture(scope="session")
def browser(playwright, browser_type_launch_args, config):
    """דפדפן - נפתח פעם אחת לכל הטסטים"""
    browser_type = config["browser"]["type"]
    
    if browser_type == "chromium":
        browser = playwright.chromium.launch(**browser_type_launch_args)
    elif browser_type == "firefox":
        browser = playwright.firefox.launch(**browser_type_launch_args)
    elif browser_type == "webkit":
        browser = playwright.webkit.launch(**browser_type_launch_args)
    else:
        browser = playwright.chromium.launch(**browser_type_launch_args)
    
    yield browser
    
    browser.close()


@pytest.fixture(scope="session")
def playwright():
    """Playwright instance"""
    with sync_playwright() as p:
        yield p


# Hooks לדוחות
def pytest_runtest_makereport(item, call):
    """הוק שרץ אחרי כל טסט - לצילום מסך במקרה של כשלון"""
    if call.when == "call":
        if call.excinfo is not None:
            # הטסט נכשל
            try:
                page = item.funcargs.get("page")
                if page:
                    screenshot_name = f"failure_{item.name}"
                    page.screenshot(path=f"screenshots/{screenshot_name}.png")
            except:
                pass
