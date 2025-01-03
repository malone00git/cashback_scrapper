import csv
import os
import json
import datetime
from supabase import create_client, Client
from extra.extract_places import parse_category

with open('../citi_custom_cash_strings.json', 'r') as f:
    strings = json.load(f)

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(url, key)

sup_file_path_categories = strings["SUP_FILE_PATH_CATEGORIES"]
local_file_categories = strings["LOCAL_FILE_CATEGORIES"]
bucket_name = strings["BUCKET_NAME"]

with open(local_file_categories, 'wb') as f:
    result = supabase.storage.from_(bucket_name).download(sup_file_path_categories)
    f.write(result)

current_year = datetime.datetime.now().year
start_of_year = datetime.date(current_year, 1, 1).strftime('%Y-%m-%d')
end_of_year = datetime.date(current_year, 12, 31).strftime('%Y-%m-%d')

# retrieve the id and card names from their respective columns
known_cards = supabase.table('known_credit_card').select('kcc_id', 'known_card_name').execute()
known_cards = known_cards.data
card_exists = 'Citi Custom Cash' in map(lambda d: d['known_card_name'], known_cards)

# if card exists, retrieve its row within the table
if card_exists:
    card_dict = next(filter(lambda d: d['known_card_name'] == 'Citi Custom Cash', known_cards))
    kcc_id = card_dict['kcc_id']
else:  # else create a new row and retrieve its id
    data_1, count_1 = supabase.table('known_credit_card').insert({'known_card_name': 'Citi Custom Cash',
                                                                  'kb_id': 3, 'kn_id': 2}).execute()
    kcc_id = data_1[1][0]['kcc_id']

known_categories = supabase.table('known_category_detail').select('kcc_id', 'cat_name', 'start_date',
                                                                  'end_date').execute().data

kcc_id_exists = kcc_id in map(lambda d: d['kcc_id'], known_categories)
start_exists = start_of_year in map(lambda d: d['start_date'], known_categories)
end_date_exists = end_of_year in map(lambda d: d['end_date'], known_categories)

# open local file categories extract categories and add their respective date ranges to the database
with open(local_file_categories) as f:
    reader = csv.reader(f)
    for row in reader:
        if reader.line_num == 1:  # get the percentage from the first row
            cat_percentage = row[0]
            cat_percentage = int(cat_percentage)
        else:
            cat_exists = row[0] in map(lambda d: d['cat_name'], known_categories)
            if kcc_id_exists and cat_exists and start_exists and end_date_exists:
                pass
            else:
                places_found = parse_category(row[0])
                place_type_string = ', '.join(places_found)
                supabase.table('known_category_detail').upsert(
                    {
                        'kcc_id': kcc_id,
                        'cat_name': row[0],
                        'cat_percentage': cat_percentage,
                        'start_date': start_of_year,
                        'end_date': end_of_year,
                        'place_type': place_type_string
                    },
                    on_conflict="kcc_id, cat_name, start_date, end_date").execute()
