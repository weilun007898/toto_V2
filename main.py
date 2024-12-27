import sys
import time
import requests
import xml.etree.ElementTree as ET
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gc

class CustomChrome(uc.Chrome):
    def __del__(self):
        try:
            super().__del__()
        except OSError:
            pass

def setup_driver():
    """Initialize and return the custom undetected-chromedriver instance."""
    return CustomChrome()

def fetch_session_and_token():
    """Fetch sessionID and tokenCode via API."""
    base_url = "http://api.coba8.com"
    endpoint = "/betLogin.aspx"

    params = {
        "apiUser": "a9966",
        "apiPass": "U6N5eg",
        "user": "3836",
        "pass": "996688"
    }

    response = requests.get(base_url + endpoint, params=params)
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        session_id = root.find("sessionID").text
        token_code = root.find("tokenCode").text
        return session_id, token_code
    else:
        print(f"Error: Received status code {response.status_code}")
        return None, None

def perform_actions(inputtoto, session_id, token_code):
    """Perform actions on the webpage using the provided session and input."""
    betpoint = f"https://wap.mb99.co/wap/main.aspx?user=3836&sessionID={session_id}&tokenCode={token_code}"
    driver.get(betpoint)

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class, "mmbutt2")][contains(text(), "Mobile Bet #2")]'))
        ).click()

        entry_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtEntry"))
        )
        entry_field.clear()
        entry_field.send_keys(inputtoto)

        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btnSubmit"))
        )
        submit_button.click()

        receipt_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_divReceiptBody"))
        ).text
        return receipt_text

    except Exception as e:
        print(f"Error during test execution: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please use the correct way: python main.py 'inputstr'")
        sys.exit(1)

    inputtoto = sys.argv[1]
    session_id, token_code = fetch_session_and_token()
    if not session_id or not token_code:
        print("Failed to retrieve session or token. Exiting.")
        sys.exit(1)

    driver = setup_driver()
    receipt_text = None
    try:
        receipt_text = perform_actions(inputtoto, session_id, token_code)
    finally:
        if driver:
            driver.quit()
            del driver
            gc.collect()

    # Output receipt_text to be captured by another script
    if receipt_text:
        print("Receipt: "+ receipt_text)
        sys.exit(0)
    else:
        print("ERROR")
        sys.exit(1)
