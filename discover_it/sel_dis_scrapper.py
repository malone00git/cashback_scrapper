# Import the required modules
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open("discover_it_strings.json", "r") as f:
    strings = json.load(f)

# Various strings to insert into function(s):
url_to_scrape = strings["URL_TO_SCRAPE"]
class_offer_quarter = strings["CLASS_OFFER_QUARTER"]
oq_tag_class = strings["OQ_TAG_CLASS"]
local_file_quarters = strings["LOCAL_FILE_QUARTERS"]
on_tag_class = strings["ON_TAG_CLASS"]
local_file_categories = strings["LOCAL_FILE_CATEGORIES"]

# Create a driver object using the with statement
options = webdriver.EdgeOptions()  # create an EdgeOptions object
with webdriver.Edge(options=options) as driver:  # create a driver instance with the options
    # Load the page
    driver.get(url_to_scrape)
    # Wait for the page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, class_offer_quarter)))
    # Find all the h2 tags with class "offer-quarter"
    quarter_dates = driver.find_elements(By.CSS_SELECTOR, oq_tag_class)
    quarter_dates_list = [quarter_date.get_attribute("textContent") for quarter_date in quarter_dates]

    # Open a file named "discover_it_quarters.txt" for writing using try-with-resources
    with open(local_file_quarters, "wb") as f:
        for data in quarter_dates_list:
            # Use text to extract and clean the text
            f.write(data.encode())
            f.write(b"\n")

    # Find all the h3 tags with class "offer-name"
    categories = driver.find_elements(By.CSS_SELECTOR, on_tag_class)
    category_list = [category.get_attribute("textContent") for category in categories]

    # Open a file named "discover_it_categories.txt" for writing using try-with-resources
    with open(local_file_categories, "wb") as f:
        for data in category_list:
            # Use text to extract and clean the text
            f.write(data.encode())
            f.write(b"\n")
