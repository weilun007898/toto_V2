import sys
import time

import undetected_chromedriver as uc
import requests
import xml.etree.ElementTree as ET
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip

class LoginTest:
    def __init__(self):
        self.driver = None

    def test_login(self, inputtoto):
        # Initialize undetected-chromedriver
        self.driver = uc.Chrome()

        # Base URL for the API
        base_url = "http://api.coba8.com"
        endpoint = "/betLogin.aspx"

        # Parameters for the API request
        params = {
            "apiUser": "a9966",
            "apiPass": "U6N5eg",
            "user": "3836",
            "pass": "996688"
        }

        # Fetch sessionID and tokenCode via API
        response = requests.get(base_url + endpoint, params=params)
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            session_id = root.find("sessionID").text
            token_code = root.find("tokenCode").text
            print("Session ID:", session_id)
            print("Token Code:", token_code)
        else:
            print(f"Error: Received status code {response.status_code}")
            return

        # Construct the URL with parameters
        betpoint = f"https://wap.mb99.co/wap/main.aspx?user=3836&sessionID={session_id}&tokenCode={token_code}"

        # Open the login page
        self.driver.get(betpoint)

        # Perform the test actions
        try:
            # Click on "Mobile Bet #2"
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "mmbutt2")][contains(text(), "Mobile Bet #2")]'))
            ).click()

            # Wait for and input text into #txtEntry
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "txtEntry"))
            ).send_keys(inputtoto)
            self.driver.execute_script("arguments[0].value = arguments[1];", EC, inputtoto)
            time.sleep(5)

            # Wait for and click #btnSubmit
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btnSubmit"))
            ).click()
            time.sleep(5)

            # Wait for and extract receipt content
            receipt_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_divReceiptBody"))
            ).text
            time.sleep(5)
            print("Receipt Content:")
            print(receipt_text)

        except Exception as e:
            print(f"Error during test execution: {e}")
        finally:
            # Quit the driver
            self.driver.quit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python write.py '<input_string>'")
        sys.exit(1)
    inputtoto = sys.argv[1]
    test = LoginTest()
    test.test_login(inputtoto)
