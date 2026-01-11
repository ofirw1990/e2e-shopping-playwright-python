"""
Search Results Page - דף תוצאות חיפוש
"""
from pages.base_page import BasePage
from utils.helpers import PriceParser, Logger
import allure
from typing import List
import time


class SearchResultsPage(BasePage):
    """דף תוצאות החיפוש"""
    
    # Locators - גמישים יותר כדי לתמוך בשינויים של eBay
    ITEMS_LIST = "li.s-item, [class*='s-item'], [data-view='mi']"
    ITEM_LINK = "a.s-item__link, a[href*='/itm/'], .s-item__link"
    ITEM_PRICE = ".s-item__price, [class*='s-item__price'], span[class*='price']"
    ITEM_TITLE = ".s-item__title, h3, [class*='title']"
    NEXT_PAGE_BUTTON = "a.pagination__next, a[aria-label='Go to next search page'], nav a:has-text('Next')"
    MIN_PRICE_INPUT = "input[aria-label*='Minimum Value'], input[aria-label*='Minimum']"
    MAX_PRICE_INPUT = "input[aria-label*='Maximum Value'], input[aria-label*='Maximum']"
    PRICE_SUBMIT_BUTTON = "button[aria-label='Submit price range'], button[type='submit']"
    
    def __init__(self, page):
        super().__init__(page)
        self.price_parser = PriceParser()
        self.logger = Logger()
    
    @allure.step("Get items under price: ${max_price}, limit: {limit}")
    def get_items_under_price(self, max_price: float, limit: int = 5) -> List[str]:
        """
        מחזיר רשימת URLs של פריטים במחיר נמוך מ-max_price
        עם תמיכה ב-Paging
        """
        collected_urls = []
        page_number = 1
        
        while len(collected_urls) < limit:
            self.logger.info(f"Scanning page {page_number} for items under ${max_price}")
            
            # המתנה לטעינת הדף
            time.sleep(3)
            
            # דיבאג - הדפסת URL ומצב הדף
            current_url = self.get_current_url()
            self.logger.info(f"Current URL: {current_url}")
            
            # צילום מסך לדיבאג
            if page_number == 1:
                self.take_screenshot("search_results_page")
                # הדפסת חלק מה-HTML לדיבאג
                page_text = self.page.content()
                self.logger.info(f"Page title: {self.page.title()}")
                if "captcha" in page_text.lower():
                    self.logger.error("CAPTCHA detected! Need to solve it.")
                if "sign in" in page_text.lower() and "results" not in page_text.lower():
                    self.logger.error("Might be on wrong page - check screenshot")
            
            # ניסיון למצוא פריטים עם סלקטורים שונים
            items = []
            selectors_to_try = [
                "li.s-item",
                ".srp-results li",
                "[class*='s-item']",
                "div.s-item",
                "ul li[data-view]",
                "//li[contains(@class, 's-item')]",  # XPath
            ]
            
            for selector in selectors_to_try:
                try:
                    if selector.startswith("//"):
                        # XPath
                        items = self.page.locator(f"xpath={selector}").all()
                    else:
                        items = self.page.locator(selector).all()
                    
                    if len(items) > 0:
                        self.logger.info(f"✓ Found {len(items)} items with selector: {selector}")
                        break
                except Exception as e:
                    continue
            
            if len(items) == 0:
                self.logger.error("No items found on page with any selector!")
                self.logger.error(f"URL: {current_url}")
                break
            
            for item in items:
                if len(collected_urls) >= limit:
                    break
                
                try:
                    # קריאת מחיר
                    price_element = item.locator(self.ITEM_PRICE).first
                    price_text = price_element.inner_text(timeout=5000)
                    price = self.price_parser.extract_price(price_text)
                    
                    # בדיקה אם המחיר תקין
                    if self.price_parser.is_price_valid(price, max_price):
                        # קבלת הקישור
                        link_element = item.locator(self.ITEM_LINK).first
                        url = link_element.get_attribute("href")
                        
                        if url and url not in collected_urls:
                            title = item.locator(self.ITEM_TITLE).first.inner_text(timeout=5000)
                            self.logger.info(f"Found item: {title[:50]}... - ${price}")
                            collected_urls.append(url)
                            
                except Exception as e:
                    # דילוג על פריטים שגורמים לשגיאה (מודעות וכו')
                    continue
            
            # אם אספנו מספיק - עצירה
            if len(collected_urls) >= limit:
                break
            
            # בדיקה אם יש עמוד הבא
            if self.is_visible(self.NEXT_PAGE_BUTTON):
                self.logger.info(f"Moving to next page...")
                self.click(self.NEXT_PAGE_BUTTON)
                page_number += 1
                time.sleep(2)  # המתנה לטעינת עמוד חדש
            else:
                # אין עוד עמודים
                self.logger.info(f"No more pages available. Found {len(collected_urls)} items total.")
                break
        
        # החזרת מה שנמצא (גם אם פחות מ-limit)
        return collected_urls[:limit]
    
    @allure.step("Apply price filter: max ${max_price}")
    def apply_price_filter(self, max_price: float):
        """הפעלת פילטר מחיר (אם זמין)"""
        try:
            if self.is_visible(self.MAX_PRICE_INPUT):
                self.fill(self.MAX_PRICE_INPUT, str(int(max_price)))
                
                if self.is_visible(self.PRICE_SUBMIT_BUTTON):
                    self.click(self.PRICE_SUBMIT_BUTTON)
                    time.sleep(2)
                    self.logger.info(f"Applied price filter: max ${max_price}")
        except Exception as e:
            self.logger.error(f"Could not apply price filter: {e}")
