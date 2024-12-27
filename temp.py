import cloudscraper

# Create a scraper session
scraper = cloudscraper.create_scraper()

# URL to access
url = "https://chatgpt.com/share/676d1647-58b4-8005-8fe9-3f826aac3afd"

# Make a GET request
response = scraper.get(url)

# Check response
if response.status_code == 200:
    print("Page Content:")
    print(response.text)  # HTML content of the page
else:
    print(f"Failed to bypass Cloudflare. Status Code: {response.status_code}")
