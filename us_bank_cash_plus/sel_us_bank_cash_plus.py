import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

with open('../us_bank_cash_plus_strings.json', 'r') as f:
    strings = json.load(f)

us_bank_cash_plus_url = strings['US_BANK_CASH_PLUS_URL']
local_file_categories = strings['LOCAL_FILE_CATEGORIES']
percent_pattern = strings['PERCENT_PATTERN']

options = webdriver.EdgeOptions()


def combine_list(lst):
    # initialize an empty list to store the new elements
    new_lst = []
    # initialize a variable to store the last item appended from lst
    last_appended_item_from_lst = ''
    # loop through the original list
    for i, item in enumerate(lst):
        # the last element append from lst (i.e: lst[i+1]) is equal to the current item, skip this iteration of the loop
        if last_appended_item_from_lst == item:
            continue
        # check if the item ends with 'and '
        if item.endswith('and'):
            # concatenate the item with the next item in the list
            new_item = item + ' ' + lst[i + 1]
            # keep track of the last item appended from lst[i+1]
            last_appended_item_from_lst = lst[i + 1]
            # append the new item to the new list
            new_lst.append(new_item)
        # otherwise, check if the item is not empty
        elif item != '':
            # append the item to the new list
            new_lst.append(item)
    # return the new list
    return new_lst


def filter_list(lst):
    new_list = []
    for i, item in enumerate(lst):
        this_string = str(item)
        match = re.search(percent_pattern, this_string)
        if match:
            continue
        else:
            new_list.append(item)
    return new_list


with webdriver.Edge(options=options) as driver:
    driver.get(us_bank_cash_plus_url)
    wait = WebDriverWait(driver, 30)

    earn_percentage = driver.find_elements(By.CSS_SELECTOR, 'span.text-color-usbankblue')
    earn_percentage_list = [earn.text.strip() for earn in earn_percentage]
    earn_percentage_list = [element for element in earn_percentage_list if element[0].isnumeric()]
    print(earn_percentage_list)

    top_categories_1 = driver.find_elements(By.CSS_SELECTOR, 'div.category-five')
    top_category_list_1 = [category.text.strip().split('\n') for category in top_categories_1]
    top_category_list_1 = top_category_list_1[0]
    print(top_category_list_1)

    top_categories_2 = driver.find_elements(By.CSS_SELECTOR, 'div.cashPusIconList')
    top_category_list_2 = [category.text.strip().split('\n') for category in top_categories_2]
    top_category_list_2 = top_category_list_2[0]
    print(top_category_list_2)

    two_percent_categories = driver.find_elements(By.CSS_SELECTOR, 'div.category-two')
    two_percent_category_list = [category.text.strip().split('\n') for category in two_percent_categories]
    two_percent_category_list = two_percent_category_list[0]
    two_percent_category_list = combine_list(two_percent_category_list)
    two_percent_category_list = [category for category in two_percent_category_list if category[0].isalpha()]
    two_percent_category_list = filter_list(two_percent_category_list)
    print(two_percent_category_list)

    with open(local_file_categories, 'wb') as f:
        top_percent = earn_percentage_list[0]
        f.write(top_percent.encode('utf-8'))
        print(top_percent.encode('utf-8'))
        f.write(b'\n')
        for line in top_category_list_1:
            f.write(line.encode('utf-8'))
            print(line.encode('utf-8'))
            f.write(b'\n')
        for line in top_category_list_2:
            f.write(line.encode('utf-8'))
            print(line.encode('utf-8'))
            f.write(b'\n')
        two_percent = earn_percentage_list[1]
        f.write(two_percent.encode('utf-8'))
        print(two_percent.encode('utf-8'))
        f.write(b'\n')
        for line in two_percent_category_list:
            f.write(line.encode('utf-8'))
            print(line.encode('utf-8'))
            f.write(b'\n')
