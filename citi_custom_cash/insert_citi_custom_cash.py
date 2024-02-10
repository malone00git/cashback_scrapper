import csv
import os
import json
from supabase import create_client, Client

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
# retrieve the id and card names from their respective columns
known_cards = supabase.table('known_credit_card').select('id', 'known_card_name').execute()
known_cards = known_cards.data
card_exists = 'Citi Custom Cash' in map(lambda d: d['known_card_name'], known_cards)

# if card exists, retrieve its row within the table
if card_exists:
    card_dict = next(filter(lambda d: d['known_card_name'] == 'Citi Custom Cash', known_cards))
    kcc_id = card_dict['id']
else:  # else create a new row and retrieve its id
    data_1, count_1 = supabase.table('known_credit_card').insert({'known_card_name': 'Citi Custom Cash',
                                                                  'kb_id': 101, 'kn_id': 2}).execute()
    kcc_id = data_1[1][0]['id']

# open local file categories extract categories and add their respective date ranges to the database
with open(local_file_categories) as f:
    reader = csv.reader(f)
    index = 0
    for row in reader:
        if reader.line_num == 1:  # get the percentage from the first row
            cat_percent = row[0]
            cat_percent = int(cat_percent)
        else:  # insert new category with the percentage from above
            if card_exists:
                custom_cash_cats = supabase.table('category').select('kcc_id', 'cn_id').execute()
                custom_cash_cats = custom_cash_cats.data
                curr_cat_dict = [this_dict for this_dict in custom_cash_cats if this_dict['kcc_id'] == kcc_id]
                this_id = curr_cat_dict[index]['cn_id']
                data_2, count_2 = supabase.table('category_name').update({'cat_name': row[0]}).eq(
                    'cat_name', row[0]).execute()
                supabase.table('category').update({
                    'kcc_id': kcc_id, 'cn_id': this_id, 'cat_percentage': cat_percent}).eq(
                    'kcc_id', kcc_id).eq('cn_id', this_id).execute()
                index += 1
            else:
                data_3, count_3 = supabase.table('category_name').insert({'cat_name': row[0]}).execute()
                cn_id = data_3[1][0]['id']
                supabase.table('category').insert({
                    'kcc_id': kcc_id, 'cn_id': cn_id, 'cat_percentage': cat_percent}).execute()
