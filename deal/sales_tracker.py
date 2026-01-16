import pandas as pd
import os
from datetime import datetime

# --- CONFIGURATION ---
CATEGORIES = ["Κοστούμι", "Πουκάμισο", "Παντελόνι", "Σακκάκι", "Πουλόβερ", "Γιλέκο", "Μπουφάν"]
VAT_RATE = 0.24
# Your specific Mac directory
SAVE_DIR = "/Users/nikolask/Documents/Deal_Emporio/ΠΩΛΗΣΕΙΣ"

# Create the directory if it doesn't exist
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def get_choice(options, prompt):
    print(f"\n{prompt}:")
    for i, option in enumerate(options, 1):
        print(f"[{i}] {option}")
    
    while True:
        try:
            choice = int(input("Επιλογή αριθμού: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print(f"Παρακαλώ επιλέξτε από 1 έως {len(options)}.")
        except ValueError:
            print("Λάθος είσοδος. Δώστε έναν αριθμό.")

def record_sale():
    now = datetime.now()
    date_str = now.strftime("%y%m%d")
    timestamp = now.strftime("%H:%M:%S")
    
    filename = f"{date_str}_sales.csv"
    full_path = os.path.join(SAVE_DIR, filename)
    
    print("\n" + "="*25)
    print(" ΚΑΤΑΓΡΑΦΗ ΠΩΛΗΣΗΣ")
    print("="*25)

    # 1. Category and Payment Choice
    category = get_choice(CATEGORIES, "Κατηγορία")
    payment = get_choice(["Card", "Cash"], "Τρόπος Πληρωμής")
    
    # 2. Receipt Logic (α/β)
    if payment == "Card":
        receipt = "Yes"
    else:
        while True:
            # .strip().lower() handles spaces and case sensitivity
            receipt_input = input("α / β; ").strip().lower()
            if receipt_input in ['α', 'a']: # Handles both Greek and English 'a'
                receipt = "Yes"
                break
            elif receipt_input in ['β', 'b']: # Handles both Greek and English 'b'
                receipt = "No"
                break
            else:
                print("Παρακαλώ πατήστε 'α' για Ναι ή 'β' για Όχι.")
    
    try:
        price = float(input("Συνολική Αξία (με ΦΠΑ): "))
    except ValueError:
        print(">> Σφάλμα: Μη έγκυρη τιμή.")
        return

    # 3. Save Data
    new_sale = {
        "Time": [timestamp],
        "Category": [category],
        "Payment": [payment],
        "Receipt": [receipt],
        "Price": [price]
    }
    df_new = pd.DataFrame(new_sale)

    if not os.path.isfile(full_path):
        df_new.to_csv(full_path, index=False)
    else:
        df_new.to_csv(full_path, mode='a', header=False, index=False)

    # 4. Financial Summary Calculation
    df_day = pd.read_csv(full_path)
    
    # VAT Calculation logic
    df_day['VAT_Amount'] = df_day.apply(
        lambda x: x['Price'] - (x['Price'] / (1 + VAT_RATE)) if x['Receipt'] == "Yes" else 0, 
        axis=1
    )

    total_gross = df_day['Price'].sum()
    total_vat = df_day['VAT_Amount'].sum()
    card_total = df_day[df_day['Payment']=='Card']['Price'].sum()
    cash_total = df_day[df_day['Payment']=='Cash']['Price'].sum()
    
    # 5. Display Report
    print("\n" + "-"*45)
    print(f"ΣΥΝΟΨΗ ΗΜΕΡΑΣ ({date_str})")
    print(f"Σύνολο Κάρτας:    {card_total:10.2f}€")
    print(f"Σύνολο Μετρητών:  {cash_total:10.2f}€")
    print(f"Μικτό Σύνολο:     {total_gross:10.2f}€")
    print("-" * 25)
    print(f"ΦΠΑ ΠΡΟΣ ΑΠΟΔΟΣΗ (24%): {total_vat:8.2f}€")
    print("-" * 45)

if __name__ == "__main__":
    while True:
        record_sale()
        if input("\nΝέα καταχώρηση; (y/n): ").lower() != 'y':
            break