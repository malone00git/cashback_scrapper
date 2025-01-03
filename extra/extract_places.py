import re
from extra import list_of_categories, dictionary_of_places


# Function to extract keywords from the input string
def extract_keywords(curr_line):
    # Use re.sub to remove text within parentheses
    curr_line = re.sub(r'\(.*?\)', '', curr_line)
    # Remove registered trademark symbols
    curr_line = re.sub(r'®+', '', curr_line)
    # Remove the word "select", ignoring case
    curr_line = re.sub(r'select', '', curr_line, flags=re.IGNORECASE)
    # Split the line by "and" and strip whitespace
    keywords = [item.strip() for item in curr_line.split("and")]
    # Further split by "&" and strip whitespace
    keywords = [sub_item.strip() for item in keywords for sub_item in item.split("&")]
    return keywords


def find_place_search_dictionaries(keywords, *lists):
    places_found = []
    for lst in lists[0]:
        for i, keyword in enumerate(keywords):
            if keyword in lst:
                places_found.extend(lst[keyword])
                break
    return places_found


def find_place_round_3(keywords, *lists):
    places_found = []
    for lst in lists[0]:
        matches = []
        for item in lst:
            item_lower = item.lower().replace("_", " ")
            for i, part in enumerate(keywords):
                if " " not in part:
                    if part[-1] == "s":
                        part = part[:-1]
                    pattern = r'\b{}\b'.format(part)
                    if re.search(pattern, item_lower, re.IGNORECASE):
                        matches.append(item)
                        break
        places_found.extend(matches)
    return places_found


def find_place_round_2(keywords, *lists):
    places_found = []
    for lst in lists[0]:
        matches = []
        for item in lst:
            item_lower = item.lower().replace("_", " ")
            for i, part in enumerate(keywords):
                primary_keyword = part.split(" ")[0]
                pattern = r'\b{}\b'.format(primary_keyword)
                if re.search(pattern, item_lower, re.IGNORECASE):
                    matches.append(item)
                    break
        places_found.extend(matches)
    return places_found


# Function to add matching places based on keywords
def find_place_round_1(keywords, *lists):
    places_found = []
    # Iterate through each list provided
    for lst in lists[0]:
        matches = []

        # Iterate through each item in the current list
        for item in lst:
            # Convert the item to lowercase and replace underscores with spaces
            item_lower = item.lower().replace("_", " ")

            # Iterate through each part of the keywords
            for i, part in enumerate(keywords):
                # Remove the last character if it's an 's' (to handle plural forms)
                if " " in part and part[-1] == 's':
                    part = part[:-1]

                # Use word boundaries to match whole words, ignoring case
                pattern = r'\b{}\b'.format(re.escape(part))

                # Check if the pattern matches the item
                if re.search(pattern, item_lower, re.IGNORECASE):
                    matches.append(item)
                    break  # Stop checking other parts if one matches

        # Extend the places_found list with matches from the current list
        places_found.extend(matches)

    return places_found


# Function to find and print matching places based on the input string
def parse_category(curr_line):
    # Extract keywords from the input string
    keywords = extract_keywords(curr_line)
    # List comprehension with a condition to exclude empty strings
    keywords_lower = [keyword.lower() for keyword in keywords if keyword.strip()]
    list_stack = list_of_categories.all_categories()
    # Find matching places from custom dictionaries
    dictionary_stack = dictionary_of_places.all_dictionaries()
    places_found = find_place_search_dictionaries(keywords_lower, dictionary_stack)
    # Find matching places from the provided category lists
    if not places_found:
        places_found = find_place_round_1(keywords_lower, list_stack)
    if not places_found:
        places_found = find_place_round_2(keywords_lower, list_stack)
    if not places_found:
        places_found = find_place_round_3(keywords_lower, list_stack)
    return places_found
