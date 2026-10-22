import csv
from pathlib import Path #we use pathlib to run the script from other directory
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def validate_order(row):
    required_fields = [
        "order_id",
        "customer_id",
        "product",
        "quantity",
        "price"
    ]

    for field in required_fields:
        if not row.get(field): #.get() safely retrieves a dictionary value.
            return False, f"Missing field: {field}"

    try:
        quantity = int(row["quantity"])
        price = float(row["price"])
    except ValueError:
        return False,"Quantity or price is not numeric"        

    if quantity <=0:
        return False, "Quantity must be positive"

    if price < 0:
        return False, "Price cannot be negative"

    return True, "Valid order" #return True, ... and return False, ... let a function communicate both a result and a reason.


def read_orders():
    project_root = Path(__file__).resolve().parents[2] #__file__ identifies the current Python file.
                    #.resolve() produces its absolute path.
                    #.parents[2] goes up three directory levels from main.py to your project root.
                    #/ joins path components using the appropriate path syntax for your operating system.

    file_path = project_root / "data" / "raw" /"orders.csv"

    if not file_path.exists():
        print(f"Error: File not Found:{file_path}")
        return

    orders = []
    
    # try:
    with open(file_path, "r", newline="", encoding="utf-8") as file: #try: attempt an operation that might fail.
                                                #except FileNotFoundError: handle the specific case where the file doesn't exist.
                                                #encoding="utf-8": explicitly specify the text encoding.
                                                #newline="": recommended when opening CSV files with Python's csv module.
        reader = csv.DictReader(file)

        
    
        for row in reader:

            is_valid,message = validate_order(row)

            if not is_valid:
                logging.warning("Rejected order: %s", message)
                continue

            quantity = int(row["quantity"])
            price = float(row["price"])

            order_value = quantity * price

            order = {
                "order_id": row["order_id"],
                "customer_id": row["customer_id"],
                "product": row["product"],
                "price": price,
                "order_value": order_value
                }
            
            orders.append(order)

            logging.info("Processed order: %s", row["order_id"])

            # print("Order:", row["order_id"])
            # print("Product:", row["product"])
            # print("Quantity:", quantity)
            # print("Price:", price)
            # print("Order value:", order_value)
            # print("---")
    # except FileNotFoundError:
    #     print(f"Error: File not Found:{file_path}")            
    logging.info("Total orders: %s", len(orders))
    logging.info("Total order value: %.2f",
                sum(order["order_value"] for order in orders))
read_orders()