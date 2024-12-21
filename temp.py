import cloudscraper

# Create a scraper session
scraper = cloudscraper.create_scraper()

# URL to access
url = "https://wap.mb99.co/wap/default.aspx?code="

# Make a GET request
response = scraper.get(url)

# Check response
if response.status_code == 200:
    print("Page Content:")
    print(response.text)  # HTML content of the page
else:
    print(f"Failed to bypass Cloudflare. Status Code: {response.status_code}")
