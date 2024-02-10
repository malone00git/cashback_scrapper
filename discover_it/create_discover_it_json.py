import json

# Various strings to insert into function(s):
strings = {
    "BUCKET_NAME": "known_cashback_cards",
    "LOCAL_FILE_CATEGORIES": "discover_it_categories.txt",
    "LOCAL_FILE_QUARTERS": "discover_it_quarters.txt",
    "SUP_FILE_PATH_CATEGORIES": "discover_it/categories.txt",
    "SUP_FILE_PATH_QUARTERS": "discover_it/quarters.txt",
    "OFFER_NAME_TAG_CLASS": "h3.offer-name",
    "OFFER_QUARTER_TAG_CLASS": "h2.offer-quarter",
    "UNKNOWN_CATEGORY": "Coming Soon",
    "URL_TO_SCRAPE": "https://www.discover.com/credit-cards/cash-back/cashback-calendar.html",
    "CLASS_OFFER_QUARTER": "offer-quarter",
    "OQ_TAG_CLASS": "h2.offer-quarter",
    "ON_TAG_CLASS": "h3.offer-name",
    "FOLDER_NAME": "discover_it",
    "FILE_NAME": "categories.txt",
    "HTML_PARSER": "html.parser",
    "MONTH_YEAR_PATTERN": r'([A-Za-z]+) to ([A-Za-z]+) (\d{4})'
}

with open('../discover_it_strings.json', 'w') as f:
    json.dump(strings, f, indent=4, sort_keys=True, ensure_ascii=False)
