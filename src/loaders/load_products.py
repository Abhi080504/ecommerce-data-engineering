import pandas as pd # pandas is used to read the processed CSV file into a DataFrame.
import mysql.connector
# mysql.connector allows Python to connect to a MySQL database
# and execute SQL statements.
import os
from dotenv import load_dotenv #Allows python to read the env file


from pathlib import Path # Path helps us build file paths safely on Windows and other operating systems.

# Locate the enriched CSV file
# Find the project root directory.
# __file__ is the path of this Python file.
# resolve() converts it to an absolute path.
# parents[2] moves up two directory levels:
# load_products.py -> loaders -> src -> project root.
BASE_DIR = Path(__file__).resolve().parents[2]

# Load environment variables from the project's .env file.
load_dotenv(BASE_DIR / ".env")

# Confirm that the required database configuration is available.
required_settings = ["DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD", "DB_NAME"]
missing_settings = [
    setting for setting in required_settings
    if os.getenv(setting) is None
]

if missing_settings:
    raise RuntimeError(
        f"Missing database settings in .env: {', '.join(missing_settings)}"
    )

# Build the path to the enriched CSV file.
# The / operator joins path components into one valid path.
CSV_PATH = BASE_DIR / "data" / "processed" / "products_enriched.csv"

# Read the transformed data
# Read the enriched CSV file into a Pandas DataFrame.
# Each CSV row becomes a DataFrame row, and each column becomes a DataFrame column.
df = pd.read_csv(CSV_PATH)
# Display the number of rows loaded from the CSV.
# len(df) returns the number of rows in the DataFrame.
print(f"CSV loaded successfully: {len(df)} rows")

# Initialize these variables as None.
# This allows the finally block to check whether a connection
# or cursor was successfully created before closing it.
connection = None
cursor = None

try:
    
    # Read MySQL connection settings from environment variables.
    db_config = {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "ecommerce_dw"),
        "connection_timeout": 5,
        "use_pure": True,
    }

    # Connect to MySQL using the configuration dictionary.
    connection = mysql.connector.connect(**db_config)


    # Confirm that the database connection was successful.
    print("Connected to MySQL successfully")

    # Create a cursor. Its an object python uses to send SQL commands to MySQL
    # A cursor is used to execute SQL statements against the database.
    cursor = connection.cursor()

    #Prepare the INSERT statement
    # Define the SQL INSERT statement.
    # This specifies which table columns will receive the incoming values.
    query = """
        INSERT INTO products(
        id,title,category,price,discountPercentage,
        rating,stock,brand,discounted_price
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE  
            title = VALUES(title),
            category = VALUES(category),
            price = VALUES(price),
            discountPercentage = VALUES(discountPercentage),
            rating = VALUES(rating),
            stock = VALUES(stock),
            brand = VALUES(brand),
            discounted_price = VALUES(discounted_price)
    """ #This is the Insert and Update (UPSERT) Command 
        #New product ID: MySQL inserts a new row.
        #Existing product ID: MySQL updates the existing row with the incoming product data.
        #Primary key: The existing ID remains unchanged.
        #Transaction: Your existing connection.commit() still saves the changes.


    # Convert DataFrame rows into tuples
    # Convert each DataFrame row into a tuple.
    # itertuples(index=False, name=None) returns values in column order,
    # without the DataFrame index or named-tuple wrapper.
    records = list(df.itertuples(index=False, name=None))

    #Insert all product records
    # Insert all tuples using the parameterized SQL statement.
    # executemany() applies the same INSERT statement to multiple records.
    # The %s placeholders are safely populated by the connector;
    # do not build SQL by concatenating values into the query.
    cursor.executemany(query, records)

    # Display how many records are about to be inserted.
    print(f"Attempting to insert {len(records)} records...")
   
    connection.commit()
    # Report how many rows the cursor says were affected by the UPSERT.
    print(
        f"Successfully processed {len(records)} products "
        "using MySQL upsert."
        )
    
    

except Exception as error:
    # If an error occurs after connecting, roll back uncommitted changes.
    # This helps prevent a failed transaction from leaving partial changes.
    if connection and connection.is_connected():
        connection.rollback()

    # Print the error message to help identify what went wrong.
    print(f"Data loading failed: {error}")

    # Raise the error again so the Python process reports the failure.
    # This is useful for debugging and for automated pipelines.
    raise

finally:
    # The finally block runs whether the operation succeeds or fails.

    # Close the cursor if it was created.
    # This releases resources associated with the cursor.
    if cursor:
        cursor.close()

    # Close the database connection if it was established.
    # This releases the connection instead of leaving it open.    
    if connection and connection.is_connected():
        connection.close()


# Five concepts you should understand
# 1. What is a DataFrame?
# A DataFrame is Pandas' table-like data structure. Your CSV is loaded into df, where each product is a row and each field—such as price or stock—is a column.
# 2. What is a cursor?
# A cursor is the object Python uses to send SQL commands to MySQL. For example:
# cursor = connection.cursor()cursor.execute("SELECT COUNT(*) FROM products")



# The cursor executes the SQL statement; you can then retrieve its result.
# 3. Why use %s placeholders?
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)


# These are parameter placeholders. The connector supplies the actual values from each tuple. This avoids unsafe SQL string construction and helps handle values correctly.
# 4. What is the difference between executemany() and commit()?
# - executemany() sends the insert operation for multiple records.
# - commit() saves the transaction.
# They do different jobs: executing an insert and committing it are not the same operation.
# 5. Why use try, except, and finally?
# - try: run the database operations.
# - except: handle and report errors, rolling back if appropriate.
# - finally: close the cursor and connection even if an error occurs.
# This pattern is important in real ETL pipelines because database operations can fail.
# Two improvements to remember
# 1. Protect your password. For now, replace "YOUR_PASSWORD" with your real password only in your local file. Later, we'll use an environment variable so credentials aren't embedded in source code or accidentally committed to GitHub.
# 2. Make the loader safe to rerun. Your current INSERT statement will fail on duplicate primary keys if you run it a second time with the same product IDs. That's expected behavior for a standard insert. We'll later implement a controlled reload or upsert strategy.
# Your current loader has already successfully inserted all 10 products, so you don't need to run this commented version again right now.