import pandas as pd
import os
from datetime import datetime

# --- CONFIGURATION ---
VAT_RATE = 0.24
SAVE_DIR = "/Users/nikolask/Documents/Deal_Emporio/ΠΩΛΗΣΕΙΣ"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CAT_FILE = os.path.join(SCRIPT_DIR, "categories.txt")

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def load_categories():
    default_cats = ["Κοστούμι", "Πουκάμισο", "Παντελόνι", "Σακκάκι", "Πουλόβερ", "Γιλέκο"]
    if not os.path.exists(CAT_FILE):
        with open(CAT_FILE, "w", encoding="utf-8") as f:
            for cat in default_cats: f.write(cat + "\n")
        return default_cats
    with open(CAT_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def clear_screen():
    os.system('clear')

def get_choice(options, prompt, allow_back=True):
    print(f"\n{prompt}:")
    if allow_back:
        print("[0] ΑΚΥΡΩΣΗ / ΠΙΣΩ")
    for i, option in enumerate(options, 1):
        print(f"[{i}] {option}")
    while True:
        try:
            choice = input("Επιλογή: ").strip()
            if choice == '0' and allow_back:
                return "BACK"
            choice_int = int(choice)
            if 1 <= choice_int <= len(options):
                return options[choice_int - 1]
            print(f"Επιλέξτε από 0 έως {len(options)}.")
        except ValueError:
            print("Λάθος είσοδος.")

def update_and_save(df_sales, full_path):
    summary_markers = ["---SUMMARY---", "TOTAL CARD", "TOTAL CASH", "GROSS TOTAL", "VAT TO PAY (24%)"]
    df_sales = df_sales[~df_sales['Time'].isin(summary_markers)].copy()
    
    # Calculate VAT per row: Price - (Price / 1.24)
    df_sales['VAT_Calculated'] = df_sales.apply(
        lambda x: round(x['Price'] - (x['Price'] / (1 + VAT_RATE)), 2) 
        if (x['Payment'] == "Card" or x['α/β'] == "α") else 0.0, axis=1
    )
    
    total_gross = round(df_sales['Price'].sum(), 2)
    total_vat = round(df_sales['VAT_Calculated'].sum(), 2)
    card_sum = round(df_sales[df_sales['Payment'] == 'Card']['Price'].sum(), 2)
    cash_sum = round(df_sales[df_sales['Payment'] == 'Cash']['Price'].sum(), 2)

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

def view_daily_report(full_path):
    if not os.path.exists(full_path):
        print("\n>> Δεν υπάρχουν πωλήσεις για σήμερα ακόμα.")
        return
    df = pd.read_csv(full_path)
    summary_markers = ["---SUMMARY---", "TOTAL CARD", "TOTAL CASH", "GROSS TOTAL", "VAT TO PAY (24%)"]
    df_sales = df[~df['Time'].isin(summary_markers)].copy()
    df_sales['Price'] = pd.to_numeric(df_sales['Price'], errors='coerce')

    # Recalculate VAT for the view
    df_sales['VAT_Calculated'] = df_sales.apply(
        lambda x: x['Price'] - (x['Price'] / (1 + VAT_RATE)) 
        if (x['Payment'] == "Card" or x['α/β'] == "α") else 0.0, axis=1
    )

    print("\n" + "-"*70)
    print(f"ΑΝΑΛΥΤΙΚΗ ΚΑΤΑΣΤΑΣΗ ΠΩΛΗΣΕΩΝ - {datetime.now().strftime('%d/%m/%Y')}")
    print("-" * 70)
    
    if not df_sales.empty:
        print(df_sales[['Time', 'Category', 'Payment', 'α/β', 'Price']].to_string(index=False))
        
        card_total = df_sales[df_sales['Payment'] == 'Card']['Price'].sum()
        cash_total = df_sales[df_sales['Payment'] == 'Cash']['Price'].sum()
        vat_total = df_sales['VAT_Calculated'].sum()
        grand_total = card_total + cash_total
        
        print("-" * 70)
        print(f"Σύνολο Κάρτας:   {card_total:10.2f}€")
        print(f"Σύνολο Μετρητών: {cash_total:10.2f}€")
        print(f"ΓΕΝΙΚΟ ΣΥΝΟΛΟ:   {grand_total:10.2f}€")
        print("-" * 30)
        print(f"ΣΥΝΟΛΟ ΦΠΑ (24%): {vat_total:9.2f}€")
    else:
        print("Δεν βρέθηκαν πωλήσεις.")
    print("-" * 70)

def main_menu():
    now = datetime.now()
    date_str = now.strftime("%y%m%d")
    full_path = os.path.join(SAVE_DIR, f"{date_str}_sales.csv")
    categories = load_categories()
    
    clear_screen()
    print("="*35)
    print(f"   DEAL EMPORIO - POS SYSTEM")
    print(f"   Ημερομηνία: {now.strftime('%d/%m/%Y')}")
    print("="*35)
    print("[1] Νέα Πώληση")
    print("[2] Προβολή Σημερινών Πωλήσεων")
    print("[3] Διαγραφή τελευταίας σειράς")
    print("[4] Έξοδος")
    
    cmd = input("\nΕπιλογή: ")
    
    if cmd == '1':
        basket = []
        running_total = 0.0
        while True:
            clear_screen()
            print(f"--- ΝΕΑ ΠΩΛΗΣΗ (Σύνολο: {running_total:.2f}€) ---")
            category = get_choice(categories, "Επιλέξτε Είδος (ή 0 για ακύρωση)")
            if category == "BACK": return True

            try:
                price_input = input(f"Τιμή για {category} (ή 0 για πίσω): ").strip()
                if price_input == '0': continue
                price = float(price_input)
                basket.append({"Category": category, "Price": price})
                running_total += price
            except ValueError:
                print(">> Σφάλμα τιμής."); input("Enter..."); continue
            
            cont = input(f"\nΠροσθήκη άλλου είδους; [y/n]: ").lower()
            if cont != 'y': break
        
        if not basket: return True

        payment = get_choice(["Card", "Cash"], f"Πληρωμή: {running_total:.2f}€")
        if payment == "BACK": return True

        if payment == "Card":
            receipt_status = "α"
        else:
            while True:
                r_in = input("\nα ή β; (ή 0 για ακύρωση): ").strip().lower()
                if r_in == '0': return True
                if r_in in ['α', 'a']: receipt_status = "α"; break
                elif r_in in ['β', 'b']: receipt_status = "β"; break
                else: print("Πατήστε α ή β.")

        timestamp = datetime.now().strftime("%H:%M:%S")
        new_items = [{"Time": timestamp, "Category": i["Category"], "Payment": payment, "α/β": receipt_status, "Price": i["Price"]} for i in basket]
        
        df_new = pd.DataFrame(new_items)
        if os.path.exists(full_path):
            df_existing = pd.read_csv(full_path)
            summary_markers = ["---SUMMARY---", "TOTAL CARD", "TOTAL CASH", "GROSS TOTAL", "VAT TO PAY (24%)"]
            df_sales = df_existing[~df_existing['Time'].isin(summary_markers)]
            df_final = pd.concat([df_sales, df_new], ignore_index=True)
        else:
            df_final = df_new

        update_and_save(df_final, full_path)
        input("\nΟλοκληρώθηκε. Enter...")
        
    elif cmd == '2':
        view_daily_report(full_path)
        input("\nΠιέστε Enter για επιστροφή...")
        
    elif cmd == '3':
        if os.path.exists(full_path):
            df = pd.read_csv(full_path)
            summary_markers = ["---SUMMARY---", "TOTAL CARD", "TOTAL CASH", "GROSS TOTAL", "VAT TO PAY (24%)"]
            df_sales = df[~df['Time'].isin(summary_markers)]
            if not df_sales.empty:
                update_and_save(df_sales[:-1], full_path)
                print("\n>> Διαγράφηκε.")
            else:
                print("\n>> Κενό.")
        input("\nΠιέστε Enter...")
        
    elif cmd == '4':
        return False
    return True

if __name__ == "__main__":
    while main_menu():
        pass
    clear_screen()
    print("Το πρόγραμμα τερματίστηκε. Καλή ξεκούραση!")