"""
eBay Home Page - דף הבית
"""
from pages.base_page import BasePage
import allure


class HomePage(BasePage):
    """דף הבית של eBay"""
    
    # Locators - מיקומי אלמנטים
    SEARCH_BOX = "#gh-ac"
    SEARCH_BUTTON = "#gh-btn, input[value='Search'], button[type='submit']"
    SIGN_IN_LINK = "text=Sign in"
    CART_ICON = "#gh-cart-n"
    
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://www.ebay.com"
    
    @allure.step("Open eBay home page")
    def open(self):
        """פתיחת דף הבית"""
        self.navigate_to(self.url)
        # סגירת popups
        self.close_popups()
        
    @allure.step("Search for: {query}")
    def search_item(self, query: str):
        """חיפוש מוצר"""
        # המתנה לתיבת החיפוש
        self.wait_for_element(self.SEARCH_BOX, state="visible")
        self.fill(self.SEARCH_BOX, query)
        # לחיצה על כפתור החיפוש (עם גלילה אוטומטית)
        self.click(self.SEARCH_BUTTON)
        # אלטרנטיבה: שליחה באמצעות Enter
        # self.page.locator(self.SEARCH_BOX).press("Enter")
        
    def is_logged_in(self) -> bool:
        """בדיקה אם משתמש מחובר"""
        # אם יש לינק Sign in - לא מחובר
        return not self.is_visible(self.SIGN_IN_LINK)
