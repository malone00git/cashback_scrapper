import json

strings = {
    'US_BANK_CASH_PLUS_URL': 'https://www.usbank.com/credit-cards/cash-plus-visa-signature-credit-card.html',
    'LOCAL_FILE_CATEGORIES': 'us_bank_cash_plus.txt',
    'BUCKET_NAME': 'known_cashback_cards',
    'SUP_FILE_PATH_CATEGORIES': 'us_bank_cash_plus/categories.txt',
    'FOLDER_NAME': 'us_bank_cash_plus',
    'HTML_PARSER': 'html.parser',
    'PERCENT_PATTERN': r'\d+%'
}

with open('../us_bank_cash_plus_strings.json', 'w') as f:
    json.dump(strings, f, indent=4, sort_keys=True, ensure_ascii=False)
