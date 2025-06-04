from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def search_nj_unclaimed(first_name, last_name):
    options = Options()
    # options.add_argument("--headless=new")  # Uncomment this for headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        url = "https://unclaimedproperty.nj.gov/"
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        # Step 1: Click “Search for Unclaimed Property”
        search_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Search for Unclaimed Property")))
        search_button.click()

        # Step 2: Wait for input field to appear
        wait.until(EC.presence_of_element_located((By.ID, "mat-input-0")))
        time.sleep(2)  # Let JS finish loading the full form

        # Step 3: Fill in the fields
        last_name_input = driver.find_element(By.ID, "mat-input-0")
        last_name_input.send_keys(last_name)

        first_name_input = driver.find_element(By.ID, "mat-input-1")
        first_name_input.send_keys(first_name)

        # Step 4: Click the submit button
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()

        # Step 5: Scrape results
        results = []
        cards = driver.find_elements(By.CLASS_NAME, "mat-card")
        for card in cards:
            try:
                name = card.find_element(By.CLASS_NAME, "mat-card-title").text
                address = card.find_element(By.CLASS_NAME, "mat-card-subtitle").text
                description = card.find_elements(By.TAG_NAME, "p")[0].text
                results.append({
                    "name": name,
                    "address": address,
                    "source": description
                })
            except:
                continue

        return results

    finally:
        driver.quit()

# Example usage:
data = search_nj_unclaimed("Daniel", "MacLaren")
for entry in data:
    print(entry)

