from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parents[2]

#Loading the processed dataset
input_path = project_root / "data" / "processed" / "products_cleaned.csv"

df = pd.read_csv(input_path)

# Convert columns to numeric types safely
numeric_columns = [
    "id",
    "price",
    "discountPercentage",
    "rating",
    "stock"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")
    #pd.to_numeric(..., errors="coerce") attempts to convert values into numbers.
    #"19.99" becomes 19.99.
    #"invalid" becomes NaN (a missing value).
    #NaN makes invalid numeric data easier to detect and handle in the next step.

#Remove rows with missing required values
required_columns = [
    "id","title","category","price","stock"
]

df = df.dropna(subset=required_columns)#dropna() removes rows missing essential values.

#Remove duplicate product IDs, keeping the first occurrence
df = df.drop_duplicates(subset=["id"], keep="first")#drop_duplicates() keeps only the first record for each product ID.

#Apply business validation rules
df = df[
    (df["id"] > 0)
    & (df["price"] >= 0)
    & (df["discountPercentage"].between(0,100))#between(0, 100) checks that the discount percentage is within a sensible range.
    & (df["rating"].between(0,5))#between(0, 5) checks that the rating is within the expected range.
    & (df["stock"] >= 0)
]#The other conditions reject invalid IDs, negative prices, and negative stock.

print("\nProducts after validation:", len(df))
print("Duplicate product IDs remainig:", df["id"].duplicated().sum())

# Calculate the price after discount
df["discounted_price"] = (
    df["price"] * (1 - df["discountPercentage"] / 100)
).round(2)

print("\nProduct prices after discount:")
print(df[["title", "price", "discountPercentage", "discounted_price"]].head())

print("\nData types after conversion:")
print(df.dtypes)

print("\nMissing values after conversion:")
print(df.isnull().sum())

print("Loaded products:", len(df))
print("Columns:", df.columns.tolist())
print(df.head())


output_path = (project_root / "data" / "processed" / "products_enriched.csv")

df.to_csv(output_path, index=False)

print("\nEnriched data saved to:", output_path)
print("Final rows:", len(df))
print("Final columns:", len(df.columns))