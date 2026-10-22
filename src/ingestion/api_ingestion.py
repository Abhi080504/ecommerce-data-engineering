
import requests
import json
from pathlib import Path

# The API endpoint used to retrieve 10 products.
url = "https://dummyjson.com/products?limit=10"

# Locate the project root and output file before making the request.
# This ensures the paths are defined even if the API request fails.
project_root = Path(__file__).resolve().parents[2]
output_path = project_root / "data" / "raw" / "products.json"

try:
    # Send an HTTP GET request to retrieve product data.
    # timeout=10 prevents the request from waiting indefinitely.
    response = requests.get(url, timeout=10)

    # Raise an exception if the server returns an unsuccessful status.
    response.raise_for_status()

    # Convert the JSON response into Python data structures.
    data = response.json()

    # Verify that the expected products list exists.
    if not isinstance(data.get("products"), list):
        raise ValueError("API response does not contain a valid products list")

    # Save the raw API response as readable JSON.
    # The output path points to data/raw/products.json.
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    print("Raw data saved to:", output_path)
    print("Status code:", response.status_code)
    print("Number of products:", len(data["products"]))

    # Read the saved file back to verify that it was written correctly.
    # This verification runs only after a successful API request and save.
    with open(output_path, "r", encoding="utf-8") as file:
        saved_data = json.load(file)

    # Confirm that the saved JSON contains the expected product list.
    if not isinstance(saved_data.get("products"), list):
        raise ValueError("Saved JSON does not contain a valid products list")

    print("Verified saved products:", len(saved_data["products"]))

except requests.exceptions.RequestException as error:
    # Handle connection errors, timeouts and unsuccessful HTTP responses.
    print("API request failed:", error)

    # Re-raise the error so the ETL pipeline knows this stage failed.
    raise

except (ValueError, json.JSONDecodeError) as error:
    # Handle invalid API responses or invalid JSON data.
    print("Data validation failed:", error)
    raise


#Why are we doing this?
#In Data Engineering, a successful API request doesn't necessarily prove that the output was saved correctly. Reading the file back and validating it gives us an extra quality check.