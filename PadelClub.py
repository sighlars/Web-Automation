import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Initialize Google Sheets API
def initialize_google_sheets(sheet_name):
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("path/to/credentials.json", scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name).sheet1  # Open first sheet

# Function to log reservation data to Google Sheets
def log_to_google_sheets(sheet, data):
    sheet.append_row(data)

# Initialize Selenium WebDriver
def initialize_driver():
    service = Service("path/to/chromedriver")  # Replace with your driver path
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Function to check court reservations on the club's website
def check_reservations(driver):
    driver.get("https://example-club-website.com/login")  # Replace with actual URL
    
    # Login to website (replace selectors as necessary)
    driver.find_element(By.ID, "username").send_keys("your_username")
    driver.find_element(By.ID, "password").send_keys("your_password")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(3)  # Wait for page to load
    
    # Navigate to reservations page
    driver.get("https://example-club-website.com/reservations")  # Replace with actual reservations page URL
    time.sleep(2)

    # Retrieve reservation data
    reservations = driver.find_elements(By.CLASS_NAME, "court-slot")  # Replace selector accordingly
    availability_data = [res.text for res in reservations if "available" in res.text.lower()]

    return availability_data

def main():
    sheet = initialize_google_sheets("Padel Club Reservations")
    driver = initialize_driver()
    
    try:
        while True:
            availability_data = check_reservations(driver)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data_row = [timestamp] + availability_data
            
            # Log to Google Sheets
            log_to_google_sheets(sheet, data_row)
            print(f"Logged data at {timestamp}")
            
            # Wait for 45 minutes
            time.sleep(2700)  # 45 minutes in seconds
    except KeyboardInterrupt:
        print("Automation stopped.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
