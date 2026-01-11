"""
Product Page - דף מוצר בודד
"""
from pages.base_page import BasePage
from utils.helpers import Logger
import allure
import random
import time


class ProductPage(BasePage):
    """דף מוצר"""
    
    # Locators
    ADD_TO_CART_BUTTON = "a[href*='addtocart'], button:has-text('Add to cart')"
    QUANTITY_SELECT = "select[id*='qtyTextBox']"
    SIZE_SELECT = "select[id*='msku-ds-SELECT_SIZE']"
    COLOR_SELECT = "select[id*='msku-ds-SELECT_COLOR']"
    VARIANT_BUTTONS = "div.msku-variant button"
    POPUP_CLOSE = "button[aria-label='Close']"
    GO_TO_CART_BUTTON = "a:has-text('Go to cart')"
    
    def __init__(self, page):
        super().__init__(page)
        self.logger = Logger()
    
    @allure.step("Open product: {url}")
    def open_product(self, url: str):
        """פתיחת דף מוצר"""
        self.navigate_to(url)
        time.sleep(1)
    
    @allure.step("Select random variants")
    def select_random_variants(self):
        """בחירת וריאנטים אקראיים (מידה, צבע וכו')"""
        
        # בחירת מידה אקראית
        if self.is_visible(self.SIZE_SELECT):
            self.logger.info("Selecting random size...")
            self._select_random_option(self.SIZE_SELECT)
            time.sleep(0.5)
        
        # בחירת צבע אקראי
        if self.is_visible(self.COLOR_SELECT):
            self.logger.info("Selecting random color...")
            self._select_random_option(self.COLOR_SELECT)
            time.sleep(0.5)
        
        # אם יש כפתורי וריאנט (לפעמים זה לא select אלא כפתורים)
        try:
            variant_buttons = self.page.locator(self.VARIANT_BUTTONS).all()
            if len(variant_buttons) > 0:
                random_button = random.choice(variant_buttons)
                random_button.click()
                time.sleep(0.5)
        except:
            pass
    
    def _select_random_option(self, select_locator: str):
        """בחירת אופציה אקראית מתוך select"""
        try:
            select_element = self.page.locator(select_locator).first
            options = select_element.locator("option").all()
            
            # דילוג על האופציה הראשונה (בדרך כלל "Select...")
            valid_options = [opt for opt in options[1:] if opt.get_attribute("value")]
            
            if valid_options:
                random_option = random.choice(valid_options)
                value = random_option.get_attribute("value")
                select_element.select_option(value)
                self.logger.info(f"Selected option: {random_option.inner_text()}")
        except Exception as e:
            self.logger.error(f"Could not select option: {e}")
    
    @allure.step("Add item to cart")
    def add_to_cart(self):
        """הוספת פריט לסל"""
        try:
            # המתנה לכפתור
            self.wait_for_element(self.ADD_TO_CART_BUTTON, state="visible")
            
            # לחיצה על הכפתור
            self.click(self.ADD_TO_CART_BUTTON)
            time.sleep(2)
            
            # סגירת popup אם מופיע
            if self.is_visible(self.POPUP_CLOSE):
                self.click(self.POPUP_CLOSE)
            
            self.logger.info("Item added to cart successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add to cart: {e}")
            return False
