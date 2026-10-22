import json 
from pathlib import Path
import pandas as pd

project_root  = Path(__file__).resolve().parents[2]

file_path = project_root / "data" / "raw" / "products.json"

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)#json.load(file) reads the JSON file into Python objects.

df = pd.DataFrame(data["products"])#data["products"] extracts the list of products from the API response.
        #pd.DataFrame(...) converts that list into a table.
selected_columns = [
    "id",
    "title",
    "category",
    "price",
    "discountPercentage",
    "rating",
    "stock",
    "brand"
]        

df = df[selected_columns] # Adds the selected columns in the df  

print("\nMissing Values per column:")
print(df.isnull().sum())#df.isnull().sum() counts missing values in each column.

print("\nDuplicate product IDs:", df["id"].duplicated().sum())#df["id"].duplicated().sum() counts repeated product IDs.

print("\n Data types:")
print(df.dtypes)#df.dtypes shows whether columns contain integers, decimals, text, or other data types.


print(df.head())#df.head() displays the first five rows.
print("Number of rows:", len(df))#len(df) counts the number of product records.
print("Columns:", df.columns.tolist())#df.columns.tolist() shows the column names.
#This step in Data Engineering is called DATA INSPECTION(inspecting before transforming)


# Remove products with invalid prices or stock values
df = df[(df["price"] >= 0) & (df["stock"] >= 0)] #df["price"] >= 0 keeps products with non-negative prices.
                                #df["stock"] >= 0 keeps products with non-negative stock.
                                #& means both conditions must be true.

# Save the cleaned Dataset
output_path = project_root / "data" / "processed" / "products_cleaned.csv"

df.to_csv(output_path, index=False)#to_csv(..., index=False) saves the table without adding Pandas' row index as an extra column.

verified_df = pd.read_csv(output_path)

print("Verified rows:", len(verified_df))
print("Verified columns:", len(verified_df.columns))

print("\nCLeaned data saved to:", output_path)
print("Final product count:", len(df))