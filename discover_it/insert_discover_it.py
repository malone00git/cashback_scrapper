import csv
import os
import datetime
import calendar
import re
import json
from supabase import create_client, Client

with open("discover_it_strings.json", "r") as f:
    strings = json.load(f)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

sup_file_path_categories = strings["SUP_FILE_PATH_CATEGORIES"]
sup_file_path_quarters = strings["SUP_FILE_PATH_QUARTERS"]
local_file_categories = strings["LOCAL_FILE_CATEGORIES"]
local_file_quarters = strings["LOCAL_FILE_QUARTERS"]
bucket_name = strings["BUCKET_NAME"]
month_year_pattern = strings["MONTH_YEAR_PATTERN"]
unknown_category = strings["UNKNOWN_CATEGORY"]

# download categories file from the database
with open(local_file_categories, "wb+") as f:
    result = supabase.storage.from_(bucket_name).download(sup_file_path_categories)
    f.write(result)

# download quarters file form the database
with open(local_file_quarters, "wb+") as f:
    result = supabase.storage.from_(bucket_name).download(sup_file_path_quarters)
    f.write(result)

# empty list to store the formatted dates for database insertion
formatted_dates = []

with open(local_file_quarters) as f:
    reader = csv.reader(f)
    for row in reader:

        for month_range in row:
            # Use re.search to find the matching groups in the string
            match = re.search(month_year_pattern, month_range)
            # If there is a match, assign the groups to variables
            if match:
                start_month, end_month, year = match.groups()
                # Convert the year to integer
                year = int(year)
                # Get the month number from the start month
                start_month_num = datetime.datetime.strptime(start_month, '%B').month
                # Get the month number from the end month
                end_month_num = datetime.datetime.strptime(end_month, '%B').month
                # Get the last day of the end month using calendar.monthrange
                end_month_day = calendar.monthrange(year, end_month_num)[1]
                # Format the start date as yyyy-mm-dd
                start_date = f'{year}-{start_month_num:02d}-01'
                # Format the end date as yyyy-mm-dd
                end_date = f'{year}-{end_month_num:02d}-{end_month_day}'
                # Append the start and end dates to the formatted dates list
                formatted_dates.append([start_date, end_date])

# retrieve the id and card names from their respective columns
known_cards = supabase.table('known_credit_card').select('id', 'known_card_name').execute()
known_cards = known_cards.data
card_exists = 'Discover It' in map(lambda d: d['known_card_name'], known_cards)

# if card exists, retrieve its row within the table
if card_exists:
    card_dict = next(filter(lambda d: d['known_card_name'] == 'Discover It', known_cards))
    kcc_id = card_dict['id']
else:
    data1, count = supabase.table("known_credit_card").insert({"known_card_name": "Discover It",
                                                               'kb_id': 123, 'kn_id': 4}).execute()
    kcc_id = data1[1][0]['id']

with open(local_file_categories) as f:
    reader = csv.reader(f)
    index = 0
    for row in reader:  # for each line within the file
        if row[0] != unknown_category:  # skip 'Coming soon' rows
            start_month = formatted_dates[index][0]
            end_month = formatted_dates[index][1]

            # extract known dates from the database
            known_category_data = supabase.table('category').select('kcc_id', 'start_date', 'end_date').execute()
            known_category_data = known_category_data.data

            # check to see if the id, start, and end date exists within the database
            start_exists = start_month in map(lambda d: d['start_date'], known_category_data)
            end_exists = end_month in map(lambda d: d['end_date'], known_category_data)
            id_exists = kcc_id in map(lambda d: d['kcc_id'], known_category_data)

            # if kcc_id, start date, end date exists within category table do not insert
            if start_exists and end_exists and id_exists:
                pass
            else:  # else insert new category
                data2, count = supabase.table("category_name").insert({"cat_name": row[0]}).execute()
                cn_id = data2[1][0]["id"]
                supabase.table("category").insert({"kcc_id": kcc_id, "cn_id": cn_id, "cat_percentage": 5,
                                                   "start_date": start_month, "end_date": end_month}).execute()
        index += 1
