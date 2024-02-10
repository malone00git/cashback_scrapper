# Import the required modules
import os
import urllib.parse
import json
import http.client
from supabase import create_client, Client
from bs4 import BeautifulSoup

with open("../discover_it_strings.json", "r") as f:
    strings = json.load(f)

credit_card_url = os.getenv("DISCOVER_IT_URL")
offer_quarter_tag_class = strings["OFFER_QUARTER_TAG_CLASS"]
local_file_quarters = strings["LOCAL_FILE_QUARTERS"]
bucket_name = strings["BUCKET_NAME"]
sup_file_path_quarters = strings["SUP_FILE_PATH_QUARTERS"]
offer_name_tag_class = strings["OFFER_NAME_TAG_CLASS"]
local_file_categories = strings["LOCAL_FILE_CATEGORIES"]
sup_file_path_categories = strings["SUP_FILE_PATH_CATEGORIES"]
folder_name = strings["FOLDER_NAME"]
file_name = strings["FILE_NAME"]
html_parser = strings["HTML_PARSER"]

# Initialize the supabase client with url and key
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Setup scraper API call using requests
# api_key = os.getenv("API_KEY")
# api_url = os.getenv("API_URL")

ant_api_key = os.getenv('ANT_API_KEY')
ant_api_url_1 = os.getenv('ANT_API_URL_1')
ant_api_url_2 = os.getenv('ANT_API_URL_2')

conn = http.client.HTTPSConnection(ant_api_url_1)
payload = {'url': credit_card_url, 'x-api-key': ant_api_key}
query = urllib.parse.urlencode(payload)
conn.request('GET', ant_api_url_2 + query)
response = conn.getresponse()

# payload = {"api_key": api_key, "url": credit_card_url, "render": "true"}
# response = requests.get(api_url, params=payload)

# Check if the request was successful
if response.status == 200:

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.read(), html_parser)

    # Find all the h2 tags with class "offer-quarter"
    quarter_dates = soup.select(offer_quarter_tag_class)
    quarter_dates_list = [quarter_date.getText() for quarter_date in quarter_dates]
    print(quarter_dates_list)

    # Create or get a file

    # Open a file named "discover_quarters.txt" for writing using try-with-resources
    with open(local_file_quarters, "wb") as f:
        for data in quarter_dates_list:
            # Extract the month part of the string
            month_part = " ".join(data.split(" ", 3)[:3])
            # Extract the year part of the string
            year_part = data.split(" ")[-1][-4:]
            # Combine both parts to create the desired date string
            date_string = month_part + " " + year_part
            f.write(date_string.encode())
            f.write(b"\n")

    bucket_folders = supabase.storage.from_(bucket_name).list()
    folder_exists = folder_name in map(lambda d: d["name"], bucket_folders)

    # Reopen the file in binary mode
    with open(local_file_quarters, "rb") as f:
        # Update file (or create if it doesn't exist) to Supabase storage using binary mode
        if folder_exists:
            supabase.storage.from_(bucket_name).update(file=f, path=sup_file_path_quarters,
                                                       file_options={"content-type": "text/plain", "upsert": "true"})
        else:
            supabase.storage.from_(bucket_name).upload(file=f, path=sup_file_path_quarters,
                                                       file_options={"content-type": "text/plain", "upsert": "true"})

    # Find all the h3 tags with class "offer-name"
    categories = soup.select(offer_name_tag_class)
    categories_list = [category.getText() for category in categories]
    print(categories_list)

    # Open a file named "discover_categories.txt" for writing using try-with-resources
    with open(local_file_categories, "wb") as f:
        for data in categories_list:
            print(data)
            f.write(data.encode())
            f.write(b"\n")

    file_list = supabase.storage.from_(bucket_name).list(folder_name)
    file_exists = file_name in map(lambda d: d["name"], file_list)

    # Reopen the file in binary mode
    with open(local_file_categories, "rb") as f:
        # Update the file (or create if it doesn't exist) to Supabase storage using binary mode
        if file_exists:
            supabase.storage.from_(bucket_name).update(file=f, path=sup_file_path_categories,
                                                       file_options={"content-type": "text/plain", "upsert": "true"})
        else:
            supabase.storage.from_(bucket_name).upload(file=f, path=sup_file_path_categories,
                                                       file_options={"content_type": "text/plain", "upsert": "true"})

    # Use a try-finally block to delete the files
    try:
        # Do something with the files
        pass
    finally:
        # Delete the files
        os.remove(local_file_quarters)
        os.remove(local_file_categories)

else:
    # Handle the error
    print(f"Request failed with status code {response.status}")
