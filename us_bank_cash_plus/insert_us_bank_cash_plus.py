import csv
import os
import json
from supabase import create_client, Client

with open('../us_bank_cash_plus_strings.json', 'r') as f:
    strings = json.load(f)

url = os.getenv('SUPABASE_URL')
print(url)
key = os.getenv('SUPABASE_KEY')
print(key)
supabase: Client = create_client(url, key)

sup_file_path_categories = strings['SUP_FILE_PATH_CATEGORIES']
local_file_categories = strings['LOCAL_FILE_CATEGORIES']
bucket_name = strings['BUCKET_NAME']

with open(local_file_categories, 'wb') as f:
    result = supabase.storage.from_(bucket_name).download(sup_file_path_categories)
    f.write(result)

    known_cards = supabase.table('known_credit_card').select('id', 'known_card_name').execute()
    known_cards = known_cards.data
    card_exists = 'Citi Custom Cash' in map(lambda d: d['known_card_name'], known_cards)

if card_exists:
    card_dict = next(filter(lambda d: ['known_card_name'] == 'US Bank Cash Plus', known_cards))
    kcc_id = card_dict['id']
else:
    data_1, count_1 = supabase.table('known_credit_card').insert({'known_card_name': 'US Bank Cash',
                                                                  'kb_id': 51, 'kn_id': 1}).execute()
    kcc_id = data_1[1][0]['id']

with open(local_file_categories) as f:
    reader = csv.reader(f)
    index = 0
    curr_percent = 0
    for row in reader:
        # print(row[0][0])
        if reader.line_num == 1 and row[0][0].isdigit():
            curr_percent = row[0][0]
        elif row[0][0].isdigit():
            curr_percent = row[0][0]
        if card_exists:
            if not row[0][0].isdigit():  # don't insert rows that describe the amount of percentage
                us_bank_cash_plus_cats = supabase.table('category').select('kcc_id', 'cn_id').execute()
                us_bank_cash_plus_cats = us_bank_cash_plus_cats.data
                curr_cat_dict = [this_dict for this_dict in us_bank_cash_plus_cats if this_dict['kcc_id'] == kcc_id]
                this_id = curr_cat_dict[index]['cn_id']
                data_2, count_2 = supabase.table('category_name').update({'cat_name': row[0]}).eq(
                    'cat_name', row[0]).execute()
                supabase.table('category').update({
                    'kcc_id': kcc_id, 'cn_id': this_id, 'cat_percentage': curr_percent}).eq(
                    'kcc_id', kcc_id).eq('cn_id', this_id).execute()
                index += 1
        else:
            if not row[0][0].isdigit():  # don't insert rows that describe the amount of percentage
                data_3, count_3 = supabase.table('category_name').insert({'cat_name': row[0]}).execute()
                cn_id = data_3[1][0]['id']
                supabase.table('category').insert({
                    'kcc_id': kcc_id, 'cn_id': cn_id, 'cat_percentage': curr_percent}).execute()
