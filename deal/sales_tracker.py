import pandas as pd
import os
from datetime import datetime

# --- CONFIGURATION ---
VAT_RATE = 0.24
SAVE_DIR = "/Users/nikolask/Documents/Deal_Emporio/ΠΩΛΗΣΕΙΣ"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CAT_FILE = os.path.join(SCRIPT_DIR, "categories.txt")

# Ensure directories exist
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def load_categories():
    """Loads categories from a text file. Creates default if missing."""
    default_cats = ["Κοστούμι", "Πουκάμισο", "Παντελόνι", "Σακκάκι", "Πουλόβερ", "Γιλέκο"]
    if not os.path.exists(CAT_FILE):
        with open(CAT_FILE, "w", encoding="utf-8") as f:
            for cat in default_cats:
                f.write(cat + "\n")
        return default_cats
    
    with open(CAT_FILE, "r", encoding="utf-8") as f:
        # Read lines, strip whitespace, and ignore empty lines
        return [line.strip() for line in f if line.strip()]

def clear_screen():
    os.system('clear')

def get_choice(options, prompt):
    print(f"\n{prompt}:")
    for i, option in enumerate(options, 1):
        print(f"[{i}] {option}")
    while True:
        try:
            choice = int(input("Επιλογή αριθμού: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print(f"Επιλέξτε από 1 έως {len(options)}.")
        except ValueError:
            print("Λάθος είσοδος.")

def view_daily_report(full_path):
    if not os.path.exists(full_path):
        print("\n>> Δεν υπάρχουν πωλήσεις για σήμερα ακόμα.")
        return
    
    df = pd.read_csv(full_path)
    summary_markers = ["---SUMMARY---", "TOTAL CARD", "TOTAL CASH", "GROSS TOTAL", "VAT TO PAY (24%)"]
    df_sales = df[~df['Time'].isin(summary_markers)].copy()
    df_sales['Price'] = pd.to_numeric(df_sales['Price'], errors='coerce')

    print("\n" + "-"*65)
    print(f"ΑΝΑΛΥΤΙΚΗ ΚΑΤΑΣΤΑΣΗ ΠΩΛΗΣΕΩΝ - {datetime.now().strftime('%d/%m/%Y')}")
    print("-" * 65)
    
    if len(df_sales) > 0:
        print(df_sales[['Time', 'Category', 'Payment', 'α/β', 'Price']].to_string(index=False))
        
        card_sum = df_sales[df_sales['Payment'] == 'Card']['Price'].sum()
        cash_sum = df_sales[df_sales['Payment'] == 'Cash']['Price'].sum()
        total_gross = card_sum + cash_sum
        
        print("-" * 65)
        print(f"Κάρτα: {card_sum:.2f}€ | Μετρητά: {cash_sum:.2f}€ | Σύνολο: {total_gross:.2f}€")
    else:
        print("Δεν βρέθηκαν πωλήσεις.")
    print("-" * 65)

def update_and_save(df_sales, full_path):
    summary_markers = ["---SUMMARY---", "TOTAL CARD", "TOTAL CASH", "GROSS TOTAL", "VAT TO PAY (24%)"]
    df_sales = df_sales[~df_sales['Time'].isin(summary_markers)].copy()
    
    df_sales['VAT_Calculated'] = df_sales.apply(
        lambda x: x['Price'] - (x['Price'] / (1 + VAT_RATE)) 
        if (x['Payment'] == "Card" or x['α/β'] == "α") else 0, axis=1
    )
    
    total_gross = df_sales['Price'].sum()
    total_vat = df_sales['VAT_Calculated'].sum()
    card_sum = df_sales[df_sales['Payment'] == 'Card']['Price'].sum()
    cash_sum = df_sales[df_sales['Payment'] == 'Cash']['Price'].sum()

    summary_rows = [
        {"Time": "---SUMMARY---", "Category": "", "Payment": "", "α/β": "", "Price": None},
        {"Time": "TOTAL CARD", "Category": "", "Payment": "", "α/β": "", "Price": card_sum},
        {"Time": "TOTAL CASH", "Category": "", "Payment": "", "α/β": "", "Price": cash_sum},
        {"Time": "GROSS TOTAL", "Category": "", "Payment": "", "α/β": "", "Price": total_gross},
        {"Time": "VAT TO PAY (24%)", "Category": "", "Payment": "", "α/β": "", "Price": total_vat}
    ]
    df_summary = pd.DataFrame(summary_rows)
    df_to_save = pd.concat([df_sales, df_summary], ignore_index=True)
    df_to_save.to_csv(full_path, index=False)

def main_menu():
    now = datetime.now()
    date_str = now.strftime("%y%m%d")
    full_path = os.path.join(SAVE_DIR, f"{date_str}_sales.csv")
    
    # Reload categories every time the menu opens so changes are instant
    categories = load_categories()
    
    clear_screen()
    print("="*35)
    print(f"   DEAL EMPORIO - POS SYSTEM")
    print(f"   Ημερομηνία: {now.strftime('%d/%m/%Y')}")
    print("="*35)
    print("[1] Νέα Πώληση")
    print("[2] Προβολή Σημερινών Πωλήσεων")
    print("[3] Διαγραφή τελευταίας εγγραφής")
    print("[4] Έξοδος")
    
    cmd = input("\nΕπιλογή: ")
    
    if cmd == '1':
        category = get_choice(categories, "Κατηγορία")
        payment = get_choice(["Card", "Cash"], "Τρόπος Πληρωμής")
        
        if payment == "Card":
            receipt_status = "α"
        else:
            while True:
                r_in = input("\nα ή β; ").strip().lower()
                if r_in in ['α', 'a']: receipt_status = "α"; break
                elif r_in in ['β', 'b']: receipt_status = "β"; break
                else: print("Πατήστε α ή β.")
        
        try:
            price = float(input("Συνολική Αξία (με ΦΠΑ): "))
        except ValueError:
            print(">> Σφάλμα: Μη έγκυρη τιμή.")
            input("\nΠιέστε Enter...")
            return True

        new_data = pd.DataFrame({
            "Time": [datetime.now().strftime("%H:%M:%S")],
            "Category": [category], 
            "Payment": [payment], 
            "α/β": [receipt_status], 
            "Price": [price]
        })

        if os.path.exists(full_path):
            df_existing = pd.read_csv(full_path)
            summary_markers = ["---SUMMARY---", "TOTAL CARD", "TOTAL CASH", "GROSS TOTAL", "VAT TO PAY (24%)"]
            df_sales = df_existing[~df_existing['Time'].isin(summary_markers)]
            df_final = pd.concat([df_sales, new_data], ignore_index=True)
        else:
            df_final = new_data

        update_and_save(df_final, full_path)
        input("\nΠιέστε Enter...")
        
    elif cmd == '2':
        view_daily_report(full_path)
        input("\nΠιέστε Enter για επιστροφή...")
    elif cmd == '3':
        if os.path.exists(full_path):
            df = pd.read_csv(full_path)
            summary_markers = ["---SUMMARY---", "TOTAL CARD", "TOTAL CASH", "GROSS TOTAL", "VAT TO PAY (24%)"]
            df_sales = df[~df['Time'].isin(summary_markers)]
            if len(df_sales) > 0:
                update_and_save(df_sales[:-1], full_path)
                print("\n>> Διαγράφηκε.")
            else:
                print("\n>> Κενό αρχείο.")
        input("\nΠιέστε Enter...")
    elif cmd == '4':
        return False
    return True

if __name__ == "__main__":
    while main_menu():
        pass
    clear_screen()
    print("Το πρόγραμμα τερματίστηκε. Καλή ξεκούραση!")