import os
import json
import http.client
import urllib.parse
from supabase import create_client, Client
from bs4 import BeautifulSoup


# strip categories within the list of unnecessary symbols, punctuation, and words
def format_category_list():
    for i in range(len(category_list)):
        category_list[i] = category_list[i].strip()
        category_list[i] = category_list[i].replace("(", "")
        category_list[i] = category_list[i].replace(")", "")
        category_list[i] = category_list[i].replace("*", "")
        category_list[i] = category_list[i].replace("®", "")
        category_list[i] = category_list[i].replace(replace_this_string_1, "")


with open("../chase_flex_strings.json", "r") as f:
    strings = json.load(f)

credit_card_url = strings["CHASE_FLEX_URL"]
local_file_categories = strings["LOCAL_FILE_CATEGORIES"]
local_file_quarters = strings["LOCAL_FILE_QUARTERS"]
replace_this_string_1 = strings["REPLACE_THIS_STRING_1"]
find_benefits_modal = strings["FIND_BENEFITS_MODAL"]
find_benefits_container = strings["FIND_BENEFITS_CONTAINER"]
click_hidden_modal = strings["CLICK_HIDDEN_MODAL"]
find_benefits_month_range = strings["FIND_BENEFITS_MONTH_RANGE"]
find_benefits_categories = strings["FIND_BENEFITS_CATEGORIES"]
find_benefits_year = strings['FIND_BENEFITS_YEAR']
bucket_name = strings["BUCKET_NAME"]
sup_file_path_quarters = strings["SUP_FILE_PATH_QUARTERS"]
sup_file_path_categories = strings["SUP_FILE_PATH_CATEGORIES"]
folder_name = strings["FOLDER_NAME"]
file_name = strings["FILE_NAME"]
html_parser = strings["HTML_PARSER"]

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(url, key)

# api_key = os.getenv('API_KEY')
# api_url = os.getenv('API_URL')

ant_api_key = os.getenv('ANT_API_KEY')
ant_api_url_1 = os.getenv('ANT_API_URL_1')
ant_api_url_2 = os.getenv('ANT_API_URL_2')

conn = http.client.HTTPSConnection(ant_api_url_1)
payload = {'url': credit_card_url, 'x-api-key': ant_api_key}
query = urllib.parse.urlencode(payload)
conn.request('GET', ant_api_url_2 + query)
response = conn.getresponse()

# payload = {'api_key': api_key, 'url': credit_card_url, 'render': 'true'}
# response = requests.get(api_url, params=payload)

if response.status == 200:

    # seek out the necessary data from the website and scrap it
    soup = BeautifulSoup(response.read(), html_parser)
    benefit_months = soup.select(find_benefits_month_range)
    benefit_months_list = [benefit_month.getText() for benefit_month in benefit_months]
    benefit_year_data = soup.select_one(find_benefits_year)
    string_with_year = benefit_year_data.getText()
    year_part = string_with_year.split(" ")[-1][-4:]

    # write to local quarters file
    with open(local_file_quarters, 'wb') as f:
        for data in benefit_months_list:
            months_part = data
            date_text = months_part + " " + year_part
            print(date_text)
            f.write(date_text.encode())
            f.write(b"\n")

    # check to see if the folder exists
    bucket_folders = supabase.storage.from_(bucket_name).list()
    folder_exists = folder_name in map(lambda d: d['name'], bucket_folders)

    # open local quarters file to read
    with open(local_file_quarters, 'rb') as f:
        if folder_exists:
            # if the file exist in supabase, update the content
            supabase.storage.from_(bucket_name).update(file=f, path=sup_file_path_quarters,
                                                       file_options={'content-type': 'text/plain', 'upsert': 'true'})
        else:  # else create the file, then write to it
            supabase.storage.from_(bucket_name).upload(file=f, path=sup_file_path_quarters,
                                                       file_options={'content-type': 'text/plain', 'upsert': 'true'})

    # seek out the necessary data from the website and scrap it
    categories = soup.select(find_benefits_categories)
    category_list = [category.getText() for category in categories]

    # remove unnecessary symbols, punctuation, and words
    format_category_list()

    # write to local categories file
    with open(local_file_categories, 'wb') as f:
        for data in category_list:
            f.write(data.encode())
            f.write(b'\n')

    # check to see if the file exists
    file_list = supabase.storage.from_(bucket_name).list(folder_name)
    file_exists = file_name in map(lambda d: d['name'], file_list)

    # open local categories file to read.
    with open(local_file_categories, 'rb') as f:
        # if the file exist in supabase, update the content
        if file_exists:
            supabase.storage.from_(bucket_name).update(file=f, path=sup_file_path_categories,
                                                       file_options={'content-type': 'text/plain', 'upsert': 'true'})
        else:  # else create the file, then write to it
            supabase.storage.from_(bucket_name).upload(file=f, path=sup_file_path_categories,
                                                       file_options={'content-type': 'text/plain', 'upsert': 'true'})
    try:
        pass
    finally:  # delete local categories and quarters files
        os.remove(local_file_quarters)
        os.remove(local_file_categories)

else:
    # handle the error
    print(f"Request failed with status code {response.status}")
