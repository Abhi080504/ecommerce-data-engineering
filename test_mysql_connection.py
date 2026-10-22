
import mysql.connector
import os
from dotenv import load_dotenv  # Allows Python to read the .env file.
from pathlib import Path

# Locate the project root, regardless of the terminal's current directory.
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from the project's .env file.
load_dotenv(BASE_DIR / ".env")

print("Starting MySQL connection test...", flush=True)

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

    print("Connected to MySQL successfully!", flush=True)

    # Close the connection after the test succeeds.
    connection.close()

except mysql.connector.Error as error:
    # Report connection errors without displaying the password.
    print(f"MySQL connection failed: {error}", flush=True)
    raise
