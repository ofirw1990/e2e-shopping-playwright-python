from playwright.sync_api import Page
import allure
import os
from datetime import datetime


class BasePage:
    
    def __init__(self, page: Page):
        self.page = page
        self.timeout = 30000
        
    def navigate_to(self, url: str):
        with allure.step(f"Navigate to {url}"):
            self.page.goto(url, wait_until="domcontentloaded")
            
    def click(self, locator: str):
        """לחיצה על אלמנט - עם גלילה אוטומטית"""
        element = self.page.locator(locator).first
        element.scroll_into_view_if_needed(timeout=self.timeout)
        element.click(timeout=self.timeout)
        
    def fill(self, locator: str, text: str):
        """מילוי טקסט - עם גלילה אוטומטית"""
        element = self.page.locator(locator).first
        element.scroll_into_view_if_needed(timeout=self.timeout)
        element.fill(text, timeout=self.timeout)
        
    def get_text(self, locator: str) -> str:
        return self.page.locator(locator).inner_text(timeout=self.timeout)
        
    def wait_for_element(self, locator: str, state: str = "visible"):
        self.page.locator(locator).wait_for(state=state, timeout=self.timeout)
        
    def is_visible(self, locator: str) -> bool:
        try:
            return self.page.locator(locator).is_visible(timeout=5000)
        except:
            return False
            
    def take_screenshot(self, name: str = None):
        if not name:
            name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        filepath = os.path.join(screenshot_dir, f"{name}.png")
        self.page.screenshot(path=filepath, full_page=True)
        
        with open(filepath, "rb") as image:
            allure.attach(image.read(), name=name, attachment_type=allure.attachment_type.PNG)
        
        return filepath
        
    def get_current_url(self) -> str:
        return self.page.url
    
    def close_popups(self):
        """סגירת popups נפוצים (cookies, location, וכו')"""
        import time
        time.sleep(1)  # המתנה קצרה לטעינת popups
        
        # רשימת סלקטורים נפוצים לכפתורי סגירה
        close_buttons = [
            "button:has-text('Accept')",
            "button:has-text('Accept All')",
            "button:has-text('Close')",
            "button[aria-label='Close']",
            "button[aria-label='close']",
            "[class*='close']",
            "#gdpr-banner-accept",
        ]
        
        for selector in close_buttons:
            try:
                if self.page.locator(selector).first.is_visible(timeout=2000):
                    self.page.locator(selector).first.click(timeout=2000)
                    time.sleep(0.5)
            except:
                continue
