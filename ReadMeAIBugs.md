# AI Code Review – Bug Analysis

This document describes issues found during a static review of AI-generated test automation code. The code was not executed – the review is based on reading and understanding the logic only.


## Bug 1 – Using time.sleep for waits

**Problem Description:**  
The code uses `time.sleep()` in order to wait for the page to load or for elements to appear. This is a problem because fixed sleep times are not connected to the actual state of the UI. If the page loads slower, the test may fail. If the page loads faster, the test wastes time. This often causes flaky and unstable tests.

**Problematic code:**
```python
import time
time.sleep(5)
```

**Suggested fix:**  
Instead of sleeping, wait for a real UI condition using Playwright:

```python
page.wait_for_selector("//div[contains(@class,'search-result')]")
```


## Bug 2 – Comparing prices as strings instead of numbers

**Problem Description:**  
The AI-generated code extracts prices as text and compares them directly to a numeric limit. This is a problem because string comparison is not numeric. For example, "100" can be considered smaller than "20" when compared as strings. This can cause wrong filtering and incorrect test results.

**Problematic code:**
```python
price = price_text.replace("$", "")
if price <= max_price:
    results.append(item)
```

**Suggested fix:**  
Convert the price value to a number before comparing:

```python
price = float(price_text.replace("$", "").strip())
if price <= max_price:
    results.append(item)
```


## Bug 3 – No handling of pagination in search results

**Problem Description:**  
The search logic assumes that all relevant items are found on the first results page. This is a problem because e-commerce sites usually split results across multiple pages. If there are fewer items on the first page, the function may return fewer results than expected. This does not meet the requirement to collect up to the requested number of items.

**Problematic code:**
```python
items = page.locator("//div[@class='item']").all()
return items[:limit]
```

**Suggested fix:**  
Add logic to move to the next page and continue collecting items until the limit is reached or no more pages are available:

```python
while len(results) < limit and page.locator("//a[text()='Next']").is_visible():
    page.click("//a[text()='Next']")
    page.wait_for_load_state("networkidle")
    # continue collecting items from the next page
```


## Summary

The issues above are common in AI-generated automation code. They usually relate to synchronization, data handling, and missing edge cases. By applying basic automation best practices, these problems can be avoided and the tests can become more stable and maintainable.