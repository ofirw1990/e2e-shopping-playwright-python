# eBay E2E Shopping Automation 🛒

**Playwright + Python + Pytest + Allure Reports**

אוטומציה מלאה לתרחיש קנייה ב-eBay: חיפוש מוצרים, סינון לפי מחיר, הוספה לסל ואימות סכום.

---

## 📋 תוכן עניינים
- [תיאור הפרויקט](#תיאור-הפרויקט)
- [ארכיטקטורה](#ארכיטקטורה)
- [התקנה](#התקנה)
- [הרצת הטסטים](#הרצת-הטסטים)
- [דוחות](#דוחות)
- [מבנה הפרויקט](#מבנה-הפרויקט)

---

## 🎯 תיאור הפרויקט

הפרויקט מממש 3 פונקציות מרכזיות:

### 1. `search_items_by_name_under_price(query, max_price, limit=5)`
- מחפש מוצרים לפי שם
- מסנן לפי מחיר מקסימלי
- תומך ב-**Paging** - עובר בין עמודים כדי למצוא מספיק פריטים
- מחזיר רשימת URLs של עד 5 פריטים

### 2. `add_items_to_cart(urls)`
- עובר על כל URL
- בוחר **וריאנטים אקראיים** (מידה, צבע, כמות)
- מוסיף לסל קניות
- שומר צילום מסך לכל פריט

### 3. `assert_cart_total_not_exceeds(budget_per_item, items_count)`
- פותח את סל הקניות
- מאמת שהסכום ≤ תקציב
- שומר צילום מסך של הסל

---

## 🏗️ ארכיטקטורה

### Page Object Model (POM)
כל דף באתר מיוצג ע"י מחלקה נפרדת:
- `BasePage` - מחלקת בסיס לכל הדפים
- `HomePage` - דף הבית (חיפוש)
- `SearchResultsPage` - תוצאות חיפוש (סינון, paging)
- `ProductPage` - דף מוצר (בחירת וריאנטים, הוספה לסל)
- `CartPage` - סל קניות (אימות סכום)

### OOP Principles
- **Inheritance** - כל Page יורש מ-BasePage
- **Encapsulation** - Locators ולוגיקה בתוך המחלקות
- **Single Responsibility** - כל מחלקה אחראית על דף אחד

### Data-Driven Testing
- קלטים מקובץ `test_data/search_data.json`
- ריצה על מספר תרחישים בבת אחת
- קל להוסיף תרחישים חדשים

---

## 🚀 התקנה

### דרישות מקדימות
- Python 3.10+
- pip

### שלבי התקנה

```bash
# 1. שכפול הפרויקט
git clone <repository-url>
cd e2e-shopping-playwright-python

# 2. יצירת סביבה וירטואלית (מומלץ)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 3. התקנת תלויות
pip install -r requirements.txt

# 4. התקנת דפדפני Playwright
playwright install chromium
```

---

## ▶️ הרצת הטסטים

### ריצה בסיסית
```bash
pytest tests/test_ebay_shopping.py -v
```

### ריצה עם Allure Reports
```bash
# ריצת הטסטים
pytest tests/test_ebay_shopping.py --alluredir=allure-results

# פתיחת הדוח
allure serve allure-results
```

### ריצה במקביל (מהר יותר)
```bash
pytest -n 2  # 2 workers במקביל
```

### ריצת טסט ספציפי
```bash
pytest tests/test_ebay_shopping.py::TestEbayShopping::test_search_and_add_shoes_to_cart -v
```

### ריצת טסטים לפי marker
```bash
pytest -m smoke  # רק smoke tests
```

---

## 📊 דוחות

### Allure Reports
דוחות אינטראקטיביים עם:
- צילומי מסך אוטומטיים
- Steps מפורטים
- גרפים וסטטיסטיקות
- Timeline של הריצה

```bash
allure serve allure-results
```

### Screenshots
כל צילומי המסך נשמרים ב-`screenshots/`:
- `search_results_*.png` - תוצאות חיפוש
- `item_*_added_to_cart.png` - פריט נוסף לסל
- `cart_final.png` - סל הקניות הסופי
- `failure_*.png` - במקרה של כשלון

---

## 📁 מבנה הפרויקט

```
e2e-shopping-playwright-python/
│
├── pages/                      # Page Object Model
│   ├── base_page.py           # מחלקת בסיס
│   ├── home_page.py           # דף הבית
│   ├── search_results_page.py # תוצאות חיפוש
│   ├── product_page.py        # דף מוצר
│   └── cart_page.py           # סל קניות
│
├── tests/                      # קבצי טסטים
│   └── test_ebay_shopping.py  # הטסט הראשי
│
├── utils/                      # כלי עזר
│   └── helpers.py             # פרסור מחירים, קריאת config
│
├── test_data/                  # Data-Driven
│   └── search_data.json       # תרחישי טסט
│
├── config/                     # קונפיגורציה
│   └── test_config.yaml       # הגדרות כלליות
│
├── screenshots/                # צילומי מסך
├── allure-results/            # תוצאות Allure
│
├── conftest.py                # Pytest fixtures
├── pytest.ini                 # הגדרות Pytest
├── requirements.txt           # תלויות
└── README.md                  # התיעוד הזה
```

---

## ⚙️ קונפיגורציה

### `config/test_config.yaml`
```yaml
browser:
  type: "chromium"      # chromium/firefox/webkit
  headless: false       # true לריצה ברקע
  slow_mo: 100          # עיכוב להדגמה

timeout:
  default: 30000        # 30 שניות
```

### `test_data/search_data.json`
```json
{
  "test_scenarios": [
    {
      "search_query": "shoes",
      "max_price": 220,
      "items_limit": 5
    }
  ]
}
```

---

## 🔍 פרטים טכניים

### Smart Locators
- שימוש ב-CSS Selectors ו-Text locators
- התמודדות עם אלמנטים דינמיים
- Retry mechanism מובנה

### Robust Design
- **Paging**: מעבר אוטומטי בין עמודים
- **Price Parsing**: פרסור חכם של מחירים (תומך ב-$, פסיקים וכו')
- **Variant Selection**: בחירה אקראית של מידות/צבעים
- **Error Handling**: המשך ריצה גם במקרה של כשלון בפריט בודד

### Best Practices
- ✅ Page Object Model
- ✅ OOP - Inheritance, Encapsulation, SRP
- ✅ Data-Driven Testing
- ✅ Allure Reports
- ✅ Smart Waits (לא sleep קבוע)
- ✅ Screenshots אוטומטיים

---

## 🎯 מה הטסטים בודקים?

### Smoke Test
```python
test_search_and_add_shoes_to_cart()
```
- חיפוש "shoes" עד $220
- הוספת 5 פריטים לסל
- אימות שהסכום לא עולה על 5 × $220

### Data-Driven Test
```python
test_data_driven_search()
```
- רץ על כל התרחישים מ-`search_data.json`
- מאפשר לבדוק מוצרים שונים במחירים שונים

---

## 🚧 מגבלות והנחות

1. **Guest Mode**: הטסטים רצים ללא התחברות (אורח)
2. **Currency**: כל המחירים ב-USD ($)
3. **Variant Selection**: בחירה אקראית - לא בדיקת זמינות מלאה
4. **Shipping**: לא מתחשבים בעלויות משלוח
5. **Stock**: לא בודקים זמינות במלאי לפני הוספה

---
