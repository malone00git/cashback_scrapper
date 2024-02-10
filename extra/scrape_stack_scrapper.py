# Import the required modules
import requests
from azure.storage.blob import BlobServiceClient
from bs4 import BeautifulSoup

# Create a BlobServiceClient object using the connection string
CONNECT_STR = "DefaultEndpointsProtocol=https;AccountName=cbwebscrapper;AccountKey=osVJME0f13bHiDBnW/" \
              "KZ2rQDu/Vg0pLuIVF8pB69YwO6Q+UE/gRcpA/Xc9e6OOZAU4R3ZCRdixdr+ASt1M+cXw==;EndpointSuffix=core.windows.net"

# Various strings to insert into function(s):
URL_TO_SCRAPE = "https://www.discover.com/credit-cards/cash-back/cashback-calendar.html"
CN_SCRAPPED_DATA = "scrappeddata"
CLASS_OFFER_QUARTER = "offer-quarter"
OQ_TAG_CLASS = "h2.offer-quarter"
FN_DISCOVER_QUARTERS = "discover_quarters.txt"
ON_TAG_CLASS = "h3.offer-name"
FN_DISCOVER_CATEGORIES = "discover_categories.txt"

# Your scrapestack API access key
ACCESS_KEY = "2b67c78ecb2c9b1eb017c0ecc866c407"

# The scrapestack API endpoint
API_ENDPOINT = "https://api.scrapestack.com/scrape"

# The parameters for the scraping request
params = {
    "access_key": ACCESS_KEY,
    "url": URL_TO_SCRAPE,
    "render_js": True  # Enable JavaScript rendering
}

# Send a GET request to the scrapestack API
response = requests.get(API_ENDPOINT, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all the h2 tags with class "offer-quarter"
    quarter_dates = soup.select(OQ_TAG_CLASS)

    # Create or get a ContainerClient object using the container name
    blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
    container_client = blob_service_client.get_container_client(CN_SCRAPPED_DATA)

    # Create the container if it does not exist
    if not container_client.exists():
        container_client.create_container()

    # Create or get a BlobClient object using the blob name
    blob_name = FN_DISCOVER_QUARTERS
    blob_client = container_client.get_blob_client(blob_name)

    # Open a file named "discover_quarters.txt" for writing using try-with-resources
    with open(blob_name, "wb") as f:
        for data in quarter_dates:
            # Use text to extract and clean the text
            text = data.text
            # Use write()
            f.write(text.encode())
            f.write(b"\n")
    # Reopen the file in binary mode
    with open(blob_name, "rb") as f:
        # Upload the file to the blob
        blob_client.upload_blob(f, overwrite=True)  # Add overwrite=True to supress exception:
        # BlobAlreadyExists when an uploaded file already exits.

    # Find all the h3 tags with class "offer-name"
    categories = soup.select(ON_TAG_CLASS)
    # Create or get a BlobClient object using the blob name
    blob_name = FN_DISCOVER_CATEGORIES
    blob_client = container_client.get_blob_client(blob_name)

    # Open a file named "discover_categories.txt" for writing using try-with-resources
    with open(blob_name, "wb") as f:
        for data in categories:
            # Use text to extract and clean the text
            text = data.text
            # Use write()
            f.write(text.encode())
            f.write(b"\n")
    # Reopen the file in binary mode
    with open(blob_name, "rb") as f:
        # Upload the file to the blob
        blob_client.upload_blob(f, overwrite=True)  # Add overwrite=True to supress exception:
        # BlobAlreadyExists when an uploaded file already exits.
else:
    # Handle the error
    print(f"Request failed with status code {response.status_code}")
