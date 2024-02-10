import json

strings = {
    "CHASE_FLEX_URL": "https://creditcards.chase.com/cash-back-credit-cards/freedom/flex",
    "LOCAL_FILE_QUARTERS": "chase_flex_quarters.txt",
    "LOCAL_FILE_CATEGORIES": "chase_flex_categories.txt",
    "REPLACE_THIS_STRING_1": "Same page link to footnote terms and conditions reference",
    "FIND_BENEFITS_MODAL": "a[data-show-modal='benefitsModal']",
    "CLICK_HIDDEN_MODAL": "arguments[0].click();",
    "FIND_BENEFITS_CONTAINER": "container-fluid",
    "FIND_BENEFITS_MONTH_RANGE": "h4.m-4",
    "FIND_BENEFITS_CATEGORIES": "p.bonus-text",
    "BUCKET_NAME": "known_cashback_cards",
    "SUP_FILE_PATH_CATEGORIES": "chase_flex/categories.txt",
    "SUP_FILE_PATH_QUARTERS": "chase_flex/quarters.txt",
    "FOLDER_NAME": "chase_flex",
    "FILE_NAME": "categories.txt",
    "HTML_PARSER": "html.parser",
    "FIND_BENEFITS_YEAR": "p.activate-text",
    "MONTH_YEAR_PATTERN": "([A-Za-z]+) â€“ ([A-Za-z]+) (\\d{4})",
    "UNKNOWN_CATEGORY": "Coming Soon"
}

with open("../chase_flex_strings.json", "w") as f:
    json.dump(strings, f, indent=4, sort_keys=True, ensure_ascii=False)
