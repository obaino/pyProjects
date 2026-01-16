import pandas as pd
import os
from datetime import datetime

# --- CONFIGURATION (Edit your categories here) ---
CATEGORIES = ["Suits", "Shirts", "Trousers", "Accessories", "Shoes", "Outerwear"]
PAYMENT_METHODS = ["Card", "Cash"]

def get_choice(options, prompt):
    print(f"\n{prompt}:")
    for i, option in enumerate(options, 1):
        print(f"[{i}] {option}")
    
    while True:
        try:
            choice = int(input("Select number: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print(f"Please choose 1 to {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def record_sale():
    now = datetime.now()
    date_str = now.strftime("%y%m%d")
    timestamp = now.strftime("%H:%M:%S")
    filename = f"{date_str}_sales.csv"
    
    print("\n" + "="*20)
    print(" NEW SALE ENTRY")
    print("="*20)

    # 1. Inputs using the lookup lists
    category = get_choice(CATEGORIES, "Select Category")
    payment = get_choice(PAYMENT_METHODS, "Select Payment Method")
    
    item_desc = input("\nItem Description (e.g., Blue Slim Fit): ")
    
    try:
        price = float(input("Price: "))
    except ValueError:
        print(">> Error: Invalid price.")
        return

    # 2. Save Data
    new_sale = {
        "Time": [timestamp],
        "Category": [category],
        "Description": [item_desc], 
        "Payment": [payment],
        "Price": [price]
    }
    df_new = pd.DataFrame(new_sale)

    if not os.path.isfile(filename):
        df_new.to_csv(filename, index=False)
    else:
        df_new.to_csv(filename, mode='a', header=False, index=False)

    # 3. Quick Stats
    df_day = pd.read_csv(filename)
    print("\n" + "-"*30)
    print(f"Total Card:  €{df_day[df_day['Payment']=='Card']['Price'].sum():.2f}")
    print(f"Total Cash:  €{df_day[df_day['Payment']=='Cash']['Price'].sum():.2f}")
    print(f"GRAND TOTAL: €{df_day['Price'].sum():.2f}")
    print("-"*30)

if __name__ == "__main__":
    while True:
        record_sale()
        if input("\nRecord another sale? (y/n): ").lower() != 'y':
            break