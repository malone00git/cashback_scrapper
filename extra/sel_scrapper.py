# Import the required modules
from azure.storage.blob import BlobServiceClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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

blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)

# Create a driver object using the with statement
options = webdriver.EdgeOptions()  # create an EdgeOptions object
with webdriver.Edge(options=options) as driver:  # create a driver instance with the options
    # Load the page
    driver.get(URL_TO_SCRAPE)
    # Wait for the page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, CLASS_OFFER_QUARTER)))
    # Find all the h2 tags with class "offer-quarter"
    quarter_dates = driver.find_elements(By.CSS_SELECTOR, OQ_TAG_CLASS)
    # Create or get a ContainerClient object using the container name
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
    categories = driver.find_elements(By.CSS_SELECTOR, ON_TAG_CLASS)
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
