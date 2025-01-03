import calendar
import csv
import datetime
import json
import os
import re
from supabase import create_client, Client
from extra.extract_places import parse_category

with open('../chase_flex_strings.json', 'r') as f:
    strings = json.load(f)

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(url, key)

sup_file_path_categories = strings["SUP_FILE_PATH_CATEGORIES"]
sup_file_path_quarters = strings["SUP_FILE_PATH_QUARTERS"]
local_file_categories = strings["LOCAL_FILE_CATEGORIES"]
local_file_quarters = strings["LOCAL_FILE_QUARTERS"]
bucket_name = strings["BUCKET_NAME"]
month_year_pattern = strings["MONTH_YEAR_PATTERN"]
unknown_category = strings["UNKNOWN_CATEGORY"]

# download categories file from the database
with open(local_file_categories, 'wb') as f:
    result = supabase.storage.from_(bucket_name).download(sup_file_path_categories)
    f.write(result)

# download quarters file from database
with open(local_file_quarters, 'wb') as f:
    result = supabase.storage.from_(bucket_name).download(sup_file_path_quarters)
    f.write(result)

# empty list to store the formatted dates for database insertion
formatted_dates = []

# open downloaded quarters file and convert the month range to mm/dd/yyyy format
with open(local_file_quarters) as f:
    reader = csv.reader(f)
    for row in reader:
        for month_range in row:
            # Use re.search to find the matching groups in the string
            match = re.search(month_year_pattern, month_range)
            if match:
                start_month, end_month, year = match.groups()
                year = int(year)
                start_month_num = datetime.datetime.strptime(start_month, '%B').month
                end_month_num = datetime.datetime.strptime(end_month, '%B').month
                end_month_day = calendar.monthrange(year, end_month_num)[1]
                start_date = f'{start_month_num:02d}/01/{year}'
                end_date = f'{end_month_num:02d}/{end_month_day:02d}/{year}'
                formatted_dates.append([start_date, end_date])

# retrieve the id and card names from their respective columns
known_cards = supabase.table('known_credit_card').select('kcc_id', 'known_card_name').execute()
known_cards = known_cards.data  # extract the dictionary from the tuple
card_exists = 'Chase Freedom Flex' in map(lambda d: d['known_card_name'], known_cards)

# if card exists, retrieve its row within the table
if card_exists:
    card_dict = next(filter(lambda d: d['known_card_name'] == 'Chase Freedom Flex', known_cards))
    kcc_id = card_dict['kcc_id']
else:  # else create a new row and retrieve its id
    data1, count = supabase.table('known_credit_card').insert({'known_card_name': 'Chase Freedom Flex',
                                                               'kb_id': 1, 'kn_id': 2}).execute()
    kcc_id = data1[1][0]['kcc_id']

# Reads all lines into a list
with open(local_file_categories, 'r') as f:
    lines = f.readlines()

# Process each line by splitting based on "|" character
formatted_lines = []
for line in lines:
    split_line = [item.strip() for item in line.strip().split("|")]
    formatted_lines.append(split_line)

# extract known dates from the database
known_categories = supabase.table('known_category_detail').select('kcc_id', 'cat_name',
                                                                  'start_date', 'end_date').execute().data
kcc_id_exists = kcc_id in map(lambda d: d['kcc_id'], known_categories)

index = 0
for split_line in formatted_lines:  # for each line within the file
    if split_line[0] != unknown_category:  # skip 'Coming soon' rows
        start_month = formatted_dates[index][0]
        end_month = formatted_dates[index][1]

        # extract and convert date format within formatted_date list to match that of the database's format
        start_date_obj = datetime.datetime.strptime(start_month, '%m/%d/%Y')
        converted_start_month = start_date_obj.strftime('%Y-%m-%d')

        end_date_obj = datetime.datetime.strptime(end_month, '%m/%d/%Y')
        converted_end_month = end_date_obj.strftime('%Y-%m-%d')

        # check to see if the kcc_id, start, and end date exists within the database
        start_exists = converted_start_month in map(lambda d: d['start_date'], known_categories)
        end_exists = converted_end_month in map(lambda d: d['end_date'], known_categories)

        # Process the split line items.
        # Each item separated by a comma will be inserted as a category item
        for i in range(len(split_line)):
            cat_exists = split_line[i] in map(lambda d: d['cat_name'], known_categories)
            if start_exists and end_exists and kcc_id_exists and cat_exists:
                pass
            else:
                places_found = parse_category(split_line[i].strip())
                # Convert the "list representation of a string" to a comma-separated string
                place_types_string = ', '.join(places_found)
                supabase.table('known_category_detail').upsert(
                    {
                        'kcc_id': kcc_id,
                        'cat_name': split_line[i].strip(),
                        'cat_percentage': 5,
                        'start_date': converted_start_month,
                        'end_date': converted_end_month,
                        'place_type': place_types_string
                    },
                    on_conflict="kcc_id, cat_name, start_date, end_date").execute()
    index += 1
try:
    pass
finally:
    os.remove(local_file_quarters)
    os.remove(local_file_categories)
