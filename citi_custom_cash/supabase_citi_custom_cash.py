import csv
import os
import json
import http.client
import urllib.parse
from supabase import create_client, Client
from bs4 import BeautifulSoup


# format the list for database entry
def format_category_list():
    # replace all commas with newline character so categories will be inserted and read from a file correctly
    for i in range(len(eligible_top_cat_list)):
        eligible_top_cat_list[i] = eligible_top_cat_list[i].replace('5% eligible categories: ', '')
        eligible_top_cat_list[i] = eligible_top_cat_list[i].replace('.', '')
        eligible_top_cat_list[i] = eligible_top_cat_list[i].replace('2', '')
        eligible_top_cat_list[i] = eligible_top_cat_list[i].strip()
        eligible_top_cat_list[i] = eligible_top_cat_list[i].replace(', ', '\n')


with open('../citi_custom_cash_strings.json', 'r') as f:
    strings = json.load(f)

credit_card_url = strings['CITI_CUSTOM_CASH_URL']
html_parser = strings['HTML_PARSER']
local_file_categories = strings['LOCAL_FILE_CATEGORIES']
sup_file_path_categories = strings['SUP_FILE_PATH_CATEGORIES']
bucket_name = strings['BUCKET_NAME']
folder_name = strings['FOLDER_NAME']

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
    soup = BeautifulSoup(response.read(), html_parser)
    earn_percentage = soup.select('p.text-heading')
    earn_percentage_list = [earn.getText().strip() for earn in earn_percentage]
    earn_summary = soup.select('p.text-subheading')
    earn_summary_list = [this_summary.getText().strip() for this_summary in earn_summary]
    eligible_top_categories = soup.select('p.text-description')
    eligible_top_cat_list = [this_list.getText().strip() for this_list in eligible_top_categories]

    format_category_list()

    with open(local_file_categories, 'wb') as f:
        top_percentage = earn_percentage_list[0][0]
        f.write(top_percentage.encode())
        for line in eligible_top_cat_list:
            f.write(b'\n')
            f.write(line.title().encode())

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
    print(f"Request failed with status code {response.status}")
