#twitter_scrap.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv
import os
import time
import urllib.parse

# Load environment variables
load_dotenv()

# Get credentials from .env file
USERNAME = os.getenv('TWITTER_USERNAME')
PASSWORD = os.getenv('TWITTER_PASSWORD')

# Set up Edge options
edge_options = Options()
# edge_options.add_argument("--headless")  # Comment this out to see the browser

# Set up the Edge WebDriver
service = Service("msedgedriver.exe")  # Replace with your msedgedriver path
driver = webdriver.Edge(service=service, options=edge_options)

def wait_and_log(selector, by=By.CSS_SELECTOR, timeout=30):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
        print(f"Found element: {selector}")
        return element
    except TimeoutException:
        print(f"Timeout waiting for element: {selector}")
        print(f"Current URL: {driver.current_url}")
        return None

def login():
    driver.get("https://x.com/i/flow/login")
    print(f"Navigated to login page. Current URL: {driver.current_url}")
    time.sleep(5)  # Wait for page to load

    try:
        # Enter username
        username_field = wait_and_log("input[autocomplete='username']")
        if username_field:
            username_field.send_keys(USERNAME)
            username_field.send_keys(Keys.RETURN)
            time.sleep(2)
        
        # Check for unusual activity
        unusual_activity = wait_and_log("//span[contains(text(), 'Unusual login activity')]", By.XPATH, timeout=5)
        if unusual_activity:
            print("Detected unusual login activity prompt. You may need to log in manually.")
            return

        # Enter password
        password_field = wait_and_log("input[name='password']")
        if password_field:
            password_field.send_keys(PASSWORD)
            password_field.send_keys(Keys.RETURN)
            time.sleep(5)

        # Check if login was successful
        home_button = wait_and_log("a[aria-label='Home']")
        if home_button:
            print("Login successful")
        else:
            print("Login might have failed. Check if you're on the correct page.")

    except Exception as e:
        print(f"An error occurred during login: {str(e)}")

    print(f"Final URL after login attempt: {driver.current_url}")

def scrape_posts(url, min_posts=20):
    driver.get(url)
    print(f"Navigated to search page. Current URL: {driver.current_url}")
    time.sleep(5)  # Wait for initial load

    post_data = []  # List to store tuples of (href, time_ago)
    scroll_attempts = 0
    max_scroll_attempts = 10

    while len(post_data) < min_posts and scroll_attempts < max_scroll_attempts:
        # Find all elements with the specified class name
        elements = driver.find_elements(By.CSS_SELECTOR, "[class*='css-175oi2r r-18u37iz r-1q142lx']")

        # Extract href links and time ago
        for element in elements:
            links = element.find_elements(By.TAG_NAME, "a")
            for link in links:
                href = link.get_attribute("href")
                if href and "/status/" in href:
                    # Find the time element and get its text content
                    try:
                        time_element = element.find_element(By.TAG_NAME, "time")
                        time_ago = time_element.text
                        post_tuple = (href, time_ago)
                        if post_tuple not in post_data:
                            post_data.append(post_tuple)
                    except NoSuchElementException:
                        post_data.append((href, "Time not found"))

        print(f"Found {len(post_data)} unique posts so far")

        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new content to load
        scroll_attempts += 1

    return post_data

def construct_search_url(search_terms, account):
    base_url = "https://x.com/search?f=live&q="
    search_query = f"({'+OR+'.join(search_terms)})+(@{account})"
    encoded_query = urllib.parse.quote(search_query, safe='+()@')
    return f"{base_url}{encoded_query}&src=typed_query"

# Get user input
print("Enter search terms (separated by commas):")
search_terms = [term.strip() for term in input().split(',')]
print("Enter the Twitter account to search within (without @):")
account = input().strip()

# Construct the search URL
search_url = construct_search_url(search_terms, account)
print(f"Constructed URL: {search_url}")

# Login
login()

# Scrape posts
scraped_data = scrape_posts(search_url, min_posts=20)

# Print the extracted links with time ago
for href, time_ago in scraped_data:
    print(f"{href} - {time_ago}")

print(f"Total unique posts scraped: {len(scraped_data)}")

# Close the browser
driver.quit()