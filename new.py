import sys
import undetected_chromedriver as uc
from seleniumbase import BaseCase
import requests
import xml.etree.ElementTree as ET

# inputtoto= ("D\n#89\n4646#3")


class CustomChrome(uc.Chrome):
    def __del__(self):
        # Override to prevent double quit()
        pass

class LoginTest(BaseCase):
    def test_login(self,):
        driver = CustomChrome()
        self.driver = driver


        # Base URL for the API
        base_url = "http://api.coba8.com"
        endpoint = "/betLogin.aspx"
        # with open("RegionRecognize.txt", "r") as file:
        #     self.inputtoto = file.read().strip()

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
        self.open(betpoint)

        # Perform the test actions
        self.click('div.mmbutt2:contains("Mobile Bet #2")')
        self.wait_for_element_visible('#txtEntry', timeout=10)
        self.type('#txtEntry', inputtoto)
        self.wait_for_element_visible('#btnSubmit', timeout=10)
        self.click('#btnSubmit')

        # Extract and print the receipt content
        self.wait_for_element_visible('#ctl00_ContentPlaceHolder1_divReceiptBody', timeout=10)
        receipt_text = self.get_text('#ctl00_ContentPlaceHolder1_divReceiptBody')
        print("Receipt Content:")
        print(receipt_text)

        # Quit the driver explicitly
        driver.quit()



