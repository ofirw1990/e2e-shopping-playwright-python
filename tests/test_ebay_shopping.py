"""
Main E2E Test - eBay Shopping Flow
בודק את כל התהליך: חיפוש, סינון, הוספה לסל, אימות
"""
import pytest
import allure
import json
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from utils.helpers import Logger, ConfigReader


@allure.feature("eBay Shopping")
@allure.story("End-to-End Shopping Flow")
class TestEbayShopping:
    """מחלקת הטסט הראשית"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        """הגדרות לפני כל טסט"""
        self.page = page
        self.home_page = HomePage(page)
        self.search_page = SearchResultsPage(page)
        self.product_page = ProductPage(page)
        self.cart_page = CartPage(page)
        self.logger = Logger()
    
    def search_items_by_name_under_price(self, query: str, max_price: float, limit: int = 5) -> list:
        """
        פונקציה 1: חיפוש פריטים לפי שם ומחיר מקסימלי
        
        Args:
            query: מה לחפש (למשל "shoes")
            max_price: מחיר מקסימלי (למשל 220)
            limit: כמה פריטים להחזיר (ברירת מחדל 5)
        
        Returns:
            רשימת URLs של פריטים שעומדים בתנאי המחיר
        """
        with allure.step(f"Search for '{query}' under ${max_price}"):
            # 1. פתיחת דף הבית
            self.home_page.open()
            
            # 2. חיפוש המוצר
            self.home_page.search_item(query)
            
            # 3. (אופציונלי) הפעלת פילטר מחיר
            self.search_page.apply_price_filter(max_price)
            
            # 4. איסוף URLs של פריטים במחיר נמוך
            urls = self.search_page.get_items_under_price(max_price, limit)
            
            self.logger.info(f"Found {len(urls)} items under ${max_price}")
            
            # 5. צילום מסך של התוצאות
            self.search_page.take_screenshot(f"search_results_{query}")
            
            return urls
    
    def add_items_to_cart(self, urls: list):
        """
        פונקציה 2: הוספת פריטים לסל קניות
        
        Args:
            urls: רשימת URLs של מוצרים להוספה
        """
        with allure.step(f"Add {len(urls)} items to cart"):
            for index, url in enumerate(urls, start=1):
                try:
                    self.logger.info(f"Adding item {index}/{len(urls)} to cart...")
                    
                    # 1. פתיחת דף המוצר
                    self.product_page.open_product(url)
                    
                    # 2. בחירת וריאנטים אקראיים (מידה, צבע וכו')
                    self.product_page.select_random_variants()
                    
                    # 3. הוספה לסל
                    success = self.product_page.add_to_cart()
                    
                    if success:
                        # 4. צילום מסך
                        self.product_page.take_screenshot(f"item_{index}_added_to_cart")
                        self.logger.info(f"✓ Item {index} added successfully")
                    else:
                        self.logger.error(f"✗ Failed to add item {index}")
                    
                except Exception as e:
                    self.logger.error(f"Error adding item {index}: {e}")
                    self.product_page.take_screenshot(f"item_{index}_error")
                    continue
    
    def assert_cart_total_not_exceeds(self, budget_per_item: float, items_count: int):
        """
        פונקציה 3: אימות שסכום הסל לא עובר את התקציב
        
        Args:
            budget_per_item: תקציב לכל פריט
            items_count: כמות פריטים
        """
        with allure.step(f"Assert cart total ≤ ${budget_per_item * items_count}"):
            # 1. פתיחת סל הקניות
            self.cart_page.open_cart()
            
            # 2. חישוב תקציב כולל
            total_budget = budget_per_item * items_count
            
            # 3. אימות
            self.cart_page.assert_total_not_exceeds(total_budget)
            
            # 4. צילום מסך של הסל
            self.cart_page.take_screenshot("cart_final")
    
    @allure.title("E2E Test: Search shoes under $220 and add to cart")
    @pytest.mark.smoke
    def test_search_and_add_shoes_to_cart(self):
        """
        תרחיש מלא: חיפוש נעליים עד $220, הוספה לסל, אימות סכום
        """
        # פרמטרים
        search_query = "shoes"
        max_price = 220
        items_limit = 5
        
        # שלב 1: חיפוש
        urls = self.search_items_by_name_under_price(search_query, max_price, items_limit)
        
        # אימות שמצאנו פריטים
        assert len(urls) > 0, "No items found!"
        
        # שלב 2: הוספה לסל
        self.add_items_to_cart(urls)
        
        # שלב 3: אימות סכום
        self.assert_cart_total_not_exceeds(max_price, len(urls))
    
    @allure.title("Data-Driven Test: Multiple search scenarios")
    @pytest.mark.parametrize("test_data", ConfigReader.read_json("test_data/search_data.json")["test_scenarios"])
    def test_data_driven_search(self, test_data):
        """
        טסט Data-Driven - מריץ מספר תרחישים מקובץ JSON
        """
        # קריאת נתונים
        query = test_data["search_query"]
        max_price = test_data["max_price"]
        limit = test_data["items_limit"]
        
        # ריצת התרחיש
        urls = self.search_items_by_name_under_price(query, max_price, limit)
        
        # אימות
        assert len(urls) > 0, f"No items found for '{query}'"
        self.logger.info(f"✓ Test passed: {test_data['description']}")
