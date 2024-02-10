import json

strings = {
    "CITI_CUSTOM_CASH_URL": "https://www.citi.com/credit-cards/citi-custom-cash-credit-card",
    "LOCAL_FILE_CATEGORIES": "citi_custom_cash_categories.txt",
    'BUCKET_NAME': 'known_cashback_cards',
    'SUP_FILE_PATH_CATEGORIES': 'citi_custom_cash/categories.txt',
    'FOLDER_NAME': 'citi_custom_cash',
    'HTML_PARSER': 'html.parser'
}

with open('../citi_custom_cash_strings.json', 'w') as f:
    json.dump(strings, f, indent=4, sort_keys=True, ensure_ascii=False)
