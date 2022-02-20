import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


chrome_driver_path = "/Users/yashviradia/Development/chromedriver"
driver = webdriver.Chrome(service=Service(chrome_driver_path))

driver.get("http://orteil.dashnet.org/experiments/cookie/")

timeout = time.time() + 5
five_min = time.time() + 60*5

# finding the cookie
cookie = driver.find_element(By.ID, "cookie")

# Getting upgrade items ids
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]

# making the list of prices
selected_list = driver.find_elements(By.CSS_SELECTOR, "#store b")

while True:
    cookie.click()

    if time.time() > timeout:

        # Get all upgrade <b> tags
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []

        # Make the list of prices
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        # find the count of cookies
        money_element = driver.find_element(By.ID, "money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        # dictionary of items and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        # Upgrades that are currently affordable
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        # Purchasing the most expensive affordable upgrade
        highest_price_affordable_upgrade = max(affordable_upgrades)
        purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element(By.ID, purchase_id).click()

        timeout = time.time() + 5

    if time.time() > five_min:
        cookie_per_s = driver.find_element(By.ID, "cps").text
        print(cookie_per_s)
        break




