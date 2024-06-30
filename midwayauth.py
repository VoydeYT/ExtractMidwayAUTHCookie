import asyncio
import websockets
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Define the URL of your Midway login page
url = ''

async def get_cookies(websocket_url):
    async with websockets.connect(websocket_url) as websocket:
        await websocket.send(json.dumps({
            'id': 1,
            'method': 'Network.getAllCookies'
        }))
        response = await websocket.recv()
        cookies_response = json.loads(response)
        return cookies_response['result']['cookies']

# Get the WebSocket URL for the debugging session
response = requests.get('http://localhost:9222/json')
pages = response.json()
websocket_debugger_url = pages[0]['webSocketDebuggerUrl']

# Extract cookies using the WebSocket connection
cookies = asyncio.get_event_loop().run_until_complete(get_cookies(websocket_debugger_url))

# Debugging output to verify cookies
print("Extracted cookies:", cookies)

# Initialize the Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("C:\Program Files\Google\Chrome\Application")  # Adjust this path to your user data directory
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Navigate to the midway login page
driver.get(url)

# Add cookies to the Selenium session
for cookie in cookies:
    try:
        cookie_dict = {
            'name': cookie['name'],
            'value': cookie['value'],
            'domain': cookie['domain'],
            'path': cookie['path'],
            'expiry': cookie.get('expires'),
            'secure': cookie['secure'],
            'httpOnly': cookie.get('httpOnly', False)
        }
        driver.add_cookie(cookie_dict)
        print(f"Added cookie: {cookie_dict}")
    except Exception as e:
        print(f"Error adding cookie: {cookie['name']}, {e}")

# Refresh the page to apply cookies
driver.refresh()

# Keep the browser open to verify the result
input("Press Enter to close the browser...")

# Now you should be authenticated
print("Authenticated successfully")
