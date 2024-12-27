# https://chatgpt.com/share/6742cec7-1ee0-8005-9172-1fc47c581a1b


import requests

# Replace with the actual URL and your API key
API_URL = "https://chatgpt.com/share/6742cec7-1ee0-8005-9172-1fc47c581a1b"
API_KEY = "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"

def ask_hengheng(query):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": query
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()  # Assuming the API returns a JSON response
    else:
        raise Exception(f"API Error: {response.status_code}, {response.text}")

# Example usage
query = "MST 3339 55a"
response = ask_hengheng(query)
print("HengHeng GPT Response:", response)
