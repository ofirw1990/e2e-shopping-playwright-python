from pages.base_page import BasePage
from utils.helpers import PriceParser, Logger
import allure
import time


class CartPage(BasePage):
    
    # Locators
    CART_URL = "https://www.ebay.com/sh/sc"
    CART_ITEMS = "div.item-container"
    SUBTOTAL = "div[data-test-id='SUB_TOTAL'] span.value"
    TOTAL = "div[data-test-id='TOTAL'] span.value"
    ITEM_PRICE = "span[data-test-id='ITEM_PRICE']"
    ITEM_QUANTITY = "select[data-test-id='qty-dropdown']"
    
    def __init__(self, page):
        super().__init__(page)
        self.price_parser = PriceParser()
        self.logger = Logger()
    
    @allure.step("Open cart")
    def open_cart(self):
        """פתיחת סל הקניות"""
        self.navigate_to(self.CART_URL)
        time.sleep(2)
    
    @allure.step("Get cart total")
    def get_cart_total(self) -> float:
        """קבלת סכום כולל של הסל"""
        try:
            # ניסיון לקרוא את הסכום הכולל
            if self.is_visible(self.TOTAL):
                total_text = self.get_text(self.TOTAL)
                total = self.price_parser.extract_price(total_text)
                self.logger.info(f"Cart total: ${total}")
                return total
            
            # אם אין total, ננסה subtotal
            elif self.is_visible(self.SUBTOTAL):
                subtotal_text = self.get_text(self.SUBTOTAL)
                subtotal = self.price_parser.extract_price(subtotal_text)
                self.logger.info(f"Cart subtotal: ${subtotal}")
                return subtotal
            
            else:
                self.logger.error("Could not find cart total")
                return 0.0
                
        except Exception as e:
            self.logger.error(f"Error getting cart total: {e}")
            return 0.0
    
    @allure.step("Get cart items count")
    def get_items_count(self) -> int:
        """ספירת פריטים בסל"""
        try:
            items = self.page.locator(self.CART_ITEMS).all()
            count = len(items)
            self.logger.info(f"Items in cart: {count}")
            return count
        except:
            return 0
    
    @allure.step("Assert cart total not exceeds ${budget}")
    def assert_total_not_exceeds(self, budget: float):
        """אימות שסכום הסל לא עולה על תקציב"""
        total = self.get_cart_total()
        
        self.logger.info(f"Budget: ${budget}, Actual: ${total}")
        
        assert total <= budget, f"Cart total ${total} exceeds budget ${budget}"
        self.logger.info(f"✓ Cart total is within budget!")
