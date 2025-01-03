import csv
import os
import datetime
import calendar
import re
import json
from supabase import create_client, Client
from extra.extract_places import parse_category

with open("../discover_it_strings.json", "r") as f:
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

# Download categories file from the database
with open(local_file_categories, "wb+") as f:
    result = supabase.storage.from_(bucket_name).download(sup_file_path_categories)
    f.write(result)

# Download quarters file form the database
with open(local_file_quarters, "wb+") as f:
    result = supabase.storage.from_(bucket_name).download(sup_file_path_quarters)
    f.write(result)

# Empty list to store the formatted dates for database insertion
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

# Retrieve the id and card names from their respective columns
known_cards = supabase.table('known_credit_card').select('kcc_id', 'known_card_name').execute()
known_cards = known_cards.data
card_exists = 'Discover It' in map(lambda d: d['known_card_name'], known_cards)

# If card exists, retrieve its row within the table
if card_exists:
    card_dict = next(filter(lambda d: d['known_card_name'] == 'Discover It', known_cards))
    kcc_id = card_dict['kcc_id']
else:
    data1, count = supabase.table("known_credit_card").insert({"known_card_name": "Discover It",
                                                               'kb_id': 2, 'kn_id': 4}).execute()
    kcc_id = data1[1][0]['kcc_id']

# Extract known dates from the database
known_category_data = supabase.table('known_category_detail').select('kcc_id', 'cat_name',
                                                                     'start_date', 'end_date').execute().data
id_exists = kcc_id in map(lambda d: d['kcc_id'], known_category_data)


# Remove 'and' from the beginning of a string
def clean_row(curr_row):
    split_row = curr_row.split()
    if split_row[0] == 'and':
        curr_row = curr_row[3:].strip()
    return curr_row


with open(local_file_categories) as f:
    reader = csv.reader(f)
    index = 0
    for row in reader:  # For each line within the file
        if row[0] != unknown_category:  # Skip 'Coming soon' rows
            start_month = formatted_dates[index][0]
            end_month = formatted_dates[index][1]

            # Check to see if the id, start, and end date exists within the database
            start_exists = start_month in map(lambda d: d['start_date'], known_category_data)
            end_exists = end_month in map(lambda d: d['end_date'], known_category_data)

            for i in range(len(row)):
                cat_exists = row[i] in map(lambda d: d['cat_name'], known_category_data)
                if start_exists and end_exists and id_exists and cat_exists:
                    pass
                else:
                    this_row = row[i].strip()
                    cleaned_row = clean_row(this_row)
                    places_found = parse_category(cleaned_row)
                    place_types_string = ', '.join(places_found)
                    supabase.table("known_category_detail").upsert(
                        {
                            "kcc_id": kcc_id,
                            "cat_name": cleaned_row,
                            "cat_percentage": 5,
                            "start_date": start_month,
                            "end_date": end_month,
                            "place_type": place_types_string
                        },
                        on_conflict="kcc_id, cat_name, start_date, end_date").execute()
        index += 1
try:
    pass
finally:
    os.remove(local_file_quarters)
    os.remove(local_file_categories)
