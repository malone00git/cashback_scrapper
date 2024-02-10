# import the required modules
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open("../chase_flex_strings.json", "r") as f:
    strings = json.load(f)

chase_flex_url = strings["CHASE_FLEX_URL"]
local_file_categories = strings["LOCAL_FILE_CATEGORIES"]
local_file_quarters = strings["LOCAL_FILE_QUARTERS"]
replace_this_string_1 = strings["REPLACE_THIS_STRING_1"]
find_benefits_modal = strings["FIND_BENEFITS_MODAL"]
find_benefits_container = strings["FIND_BENEFITS_CONTAINER"]
click_hidden_modal = strings["CLICK_HIDDEN_MODAL"]
find_benefits_month_range = strings["FIND_BENEFITS_MONTH_RANGE"]
find_benefits_categories = strings["FIND_BENEFITS_CATEGORIES"]

# create a new Edge session
options = webdriver.EdgeOptions()  # create an EdgeOptions object


def format_category_list():
    for i in range(len(category_list)):
        category_list[i] = category_list[i].replace("(", "")
        category_list[i] = category_list[i].replace(")", "")
        category_list[i] = category_list[i].replace("*", "")
        category_list[i] = category_list[i].replace("®", "")
        category_list[i] = category_list[i].replace(replace_this_string_1, "")


with webdriver.Edge(options=options) as driver:  # create a driver instance with the options
    # load the page
    driver.get(chase_flex_url)
    # wait for the page to load
    wait = WebDriverWait(driver, 30)
    # locate the element that triggers the modal
    modal_link = driver.find_element(By.CSS_SELECTOR, find_benefits_modal)
    # execute a JavaScript code that clicks on the hidden modal
    driver.execute_script(click_hidden_modal, modal_link)
    # wait for the modal to appear
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, find_benefits_container)))
    # locate the element that contains the data
    benefit_months = driver.find_elements(By.CSS_SELECTOR, find_benefits_month_range)

    benefit_year_data = driver.find_element(By.CLASS_NAME, "activate-text")
    string_with_year = benefit_year_data.get_attribute("textContent")
    year_part = string_with_year.split(" ")[-1][-4:]

    with open(local_file_quarters, "wb") as f:
        for data in benefit_months:
            months_part = data.text
            date_text = months_part + " " + year_part
            f.write(date_text.encode())
            f.write(b"\n")

    # locate the element's data
    categories = driver.find_elements(By.CSS_SELECTOR, find_benefits_categories)
    print(categories)
    # get the text content of the element, including the hidden text
    category_list = [category.get_attribute("textContent") for category in categories]

    format_category_list()

    with open(local_file_categories, "wb") as f:
        for data in category_list:
            f.write(data.encode())
            f.write(b"\n")
