import os
import json
import re
from supabase import create_client, Client
from scrapingant_client import ScrapingAntClient
from bs4 import BeautifulSoup
from extra import email_scrape_failed


with open('../us_bank_cash_plus_strings.json', 'r') as f:
    strings = json.load(f)

credit_card_url = strings['US_BANK_CASH_PLUS_URL']
html_parser = strings['HTML_PARSER']
local_file_categories = strings['LOCAL_FILE_CATEGORIES']
sup_file_path_categories = strings['SUP_FILE_PATH_CATEGORIES']
bucket_name = strings['BUCKET_NAME']
folder_name = strings['FOLDER_NAME']
percent_pattern = strings['PERCENT_PATTERN']


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
        if item.endswith('and '):
            # concatenate the item with the next item in the list
            new_item = item + lst[i + 1].strip()
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


url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(url, key)

scraping_ant_token = os.getenv('SCRAPING_ANT_TOKEN')
client = ScrapingAntClient(token=scraping_ant_token)
response = client.general_request(credit_card_url)

if response.status_code == 200:

    soup = BeautifulSoup(response.content, 'html.parser')
    earn_percentage = soup.select('span.text-color-usbankblue')
    earn_percentage_list = [earn.get_text().strip() for earn in earn_percentage]
    earn_percentage_list = [element for element in earn_percentage_list if element[0].isnumeric()]
    print(earn_percentage_list)

    top_categories_1 = soup.select('div.category-five')
    top_category_list_1 = [category.get_text().strip().split('\n') for category in top_categories_1]
    top_category_list_1 = top_category_list_1[0]

    top_categories_2 = soup.select('div.cashPusIconList1')
    top_category_list_2 = [category.get_text().strip().split('\n') for category in top_categories_2]
    top_category_list_2 = top_category_list_2[0]

    two_percent_categories = soup.select('div.category-two')
    two_percent_category_list = [category.get_text().strip().split('\n') for category in two_percent_categories]
    two_percent_category_list = two_percent_category_list[0]
    two_percent_category_list = combine_list(two_percent_category_list)
    two_percent_category_list = [category for category in two_percent_category_list if category[0].isalpha()]
    two_percent_category_list = filter_list(two_percent_category_list)

    with open(local_file_categories, 'wb') as f:
        if earn_percentage_list:
            top_percent = earn_percentage_list[-2][0]
            f.write(top_percent.encode('utf-8'))
            f.write(b'\n')
            for line in top_category_list_1:
                if line != "":
                    f.write(line.encode('utf-8'))
                    f.write(b'\n')
            for line in top_category_list_2:
                if line != "":
                    f.write(line.encode('utf-8'))
                    f.write(b'\n')
            two_percent = earn_percentage_list[-1][0]
            f.write(two_percent.encode('utf-8'))
            f.write(b'\n')
            for line in two_percent_category_list:
                if line != "":
                    f.write(line.encode('utf-8'))
                    f.write(b'\n')
        else:
            top_percent = None

    bucket_folders = supabase.storage.from_(bucket_name).list()
    folder_exists = folder_name in map(lambda d: d['name'], bucket_folders)

    with open(local_file_categories, 'rb') as f:
        if folder_exists:
            supabase.storage.from_(bucket_name).update(file=f, path=sup_file_path_categories,
                                                       file_options={'content-type': 'text/plain', 'upsert': 'true'})
        else:
            supabase.storage.from_(bucket_name).upload(file=f, path=sup_file_path_categories,
                                                       file_options={'content-type': 'text/plain', 'upsert': 'true'})

else:
    # handle the error
    # this will give you just the file name
    file_name = os.path.basename(__file__)
    email_scrape_failed.curr_file_and_err_code(file_name, response.status_code)
    email_scrape_failed.send_email()
