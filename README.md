# E-commerce Data Engineering Pipeline

## Overview

A Python-based ETL (Extract, Transform, Load) pipeline that ingests e-commerce product data from an API, cleans and validates the data, enriches product records, and loads the final dataset into a MySQL data warehouse.

The project demonstrates core data engineering concepts, including data ingestion, transformation, data quality validation, database loading, logging, error handling, and pipeline orchestration.

## Architecture

```text
DummyJSON Products API
          |
          v
     Data Ingestion
          |
          v
      Raw JSON Data
          |
          v
    Data Cleaning
          |
          v
    Data Validation
    and Enrichment
          |
          v
    Processed CSV Data
          |
          v
       MySQL DW
```

## Technology Stack

- **Language:** Python
- **Data Processing:** Pandas
- **API Integration:** Requests
- **Database:** MySQL
- **Database Connector:** mysql-connector-python
- **Configuration:** python-dotenv
- **Data Formats:** JSON, CSV
- **Workflow Orchestration:** Python subprocess-based pipeline runner

## Key Features

- Retrieves product data from an external REST API.
- Saves raw API responses as JSON.
- Cleans and transforms data using Pandas.
- Validates required fields, numeric values, ratings, discounts, and product identifiers.
- Calculates discounted product prices.
- Loads enriched data into MySQL using parameterized SQL.
- Uses MySQL UPSERT logic to insert new products and update existing records.
- Implements transaction handling, rollback, and resource cleanup.
- Uses environment variables to keep database credentials out of source code.
- Orchestrates ETL stages sequentially and stops execution when a stage fails.
- Logs pipeline execution status and errors.

## Project Structure

```text
ecommerce-data-engineering/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── ingestion/
│   ├── transformation/
│   └── loaders/
├── pipeline.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup and Execution

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ecommerce-data-engineering
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```dotenv
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=ecommerce_dw
```

Replace the password placeholder with your local MySQL password. Never commit `.env` to GitHub.

### 5. Create the MySQL database

Create the `ecommerce_dw` database and the `products` table using the schema required by the loader.

### 6. Run the pipeline

```bash
python pipeline.py
```

The pipeline runs ingestion, cleaning, enrichment, and database loading in sequence.

## Data Quality

The pipeline checks for missing values, duplicate product identifiers, invalid numeric values, and invalid rating or discount ranges before loading the enriched data.

## Future Improvements

- Orchestrate workflows using Apache Airflow.
- Add automated unit and integration tests.
- Containerize the application using Docker.
- Improve retry handling and pipeline monitoring.
- Add scheduled execution and more comprehensive data quality reporting.

## Disclaimer

This project uses sample e-commerce product data from the DummyJSON API for educational purposes.
