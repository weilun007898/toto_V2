import requests
from bs4 import BeautifulSoup
from seleniumbase import BaseCase

# Step 1: Define URLs
login_url = "https://wap.mb99.co/wap/"
bet_url = "https://wap.mb99.co//wap/main.aspx"

# Step 2: Start a session
session = requests.Session()
response = session.get(bet_url)
soup = BeautifulSoup(response.text, "html.parser")

# Step 3: Extract hidden fields
viewstate = soup.find("input", {"name": "__VIEWSTATE"})["value"]
eventvalidation = soup.find("input", {"name": "__EVENTVALIDATION"})["value"]
viewstategenerator = soup.find("input", {"name": "__VIEWSTATEGENERATOR"})["value"]

# Step 4: Prepare form data
form_data = {
    "__VIEWSTATE": viewstate,
    "__EVENTVALIDATION": eventvalidation,
    "__VIEWSTATEGENERATOR": viewstategenerator,
    "__EVENTTARGET": "",  # Often empty for ASP.NET forms
    "__EVENTARGUMENT": "",  # Often empty for ASP.NET forms
    "txtLoginName": "3836",  # Username field
    "txtLoginPassword": "996688",  # Password field
    "btnLogin": "登录",  # Login button
}

dataInput = "D\n#8\n8787#1"

# Step 5: Submit the form
submit_response = session.post(bet_url, data=form_data)

# Step 6: Check if the login was successful
if submit_response.status_code == 200:  #登录成功
    print(submit_response.text)
    print("Login successful!")
    # Optionally print the response to debug
    # print(submit_response.text)

    # Now navigate to the bet URL
    bet_response = session.post(bet_url)
    if bet_response.status_code == 200:
        print(bet_response.text)
        form_data1 = {
            "ctl00$ContentPlaceHolder1$txtEntry": dataInput,
            "ctl00$ContentPlaceHolder1$btnSubmit": "下注"
        }
        # betreturn_response = session.post(bet_url, data=form_data1)
        # if betreturn_response.status_code == 200:
        #     print("here2")
        #     print(betreturn_response.text)
        #     soup1 = BeautifulSoup(betreturn_response.text, "html.parser")
        #     print(soup1.text)
        #     receipt = soup1.find("div", {"id": "ctl00_ContentPlaceHolder1_divReceiptBody"})
        #     if receipt:
        #         result = receipt.get_text(strip=True)  # `strip=True` removes leading/trailing whitespace
        #         print(result)
        #     else:
        #         print("Receipt not found")
        # else:
        #     print("fail")
    else:
        print(f"Failed to navigate to the bet page. Status code: {bet_response.status_code}")
else:
    print(f"Login failed. Status code: {submit_response.status_code}")
    print("Response Content:", submit_response.text)

https://wap.mb99.co/wap/mobilebet.aspx?user=3836&sessionID=uwlbdftslay3kshnfrii2mqv&tokenCode=D36AA965-E78D-42F1-87E2-4F3318A75C7F