import pandas as pd
import os
from datetime import datetime

# --- CONFIGURATION ---
SAVE_DIR = "/Users/nikolask/Documents/Deal_Emporio/ΠΩΛΗΣΕΙΣ"
SCRIPT_DIR = "/Users/nikolask/Myfiles/gitPython/pyProjects/deal"
CAT_FILE = os.path.join(SCRIPT_DIR, "categories.txt")

# ANSI Color codes
BRIGHT_GREEN = '\033[92m'
DARK_GREEN = '\033[32m'
RED = '\033[91m'
RESET = '\033[0m'

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

def get_current_path():
    date_str = datetime.now().strftime("%y%m%d")
    return os.path.join(SAVE_DIR, f"{date_str}_sales.csv")

def get_last_sale_info(full_path):
    if not os.path.exists(full_path):
        return "No sales yet today."
    try:
        df = pd.read_csv(full_path)
        invalid_keywords = ["SUMMARY", "TOTAL CARD", "TOTAL CASH", "GROSS TOTAL", "VAT"]
        df_sales = df[~df['Time'].str.contains('|'.join(invalid_keywords), case=False, na=False)]
        
        if not df_sales.empty:
            last = df_sales.iloc[-1]
            time_val = str(last['Time'])
            if "TOTAL-" in time_val:
                display_time = time_val.replace('TOTAL-', '')
                return f"{display_time} | TOTAL | {last['Payment']} | {last.get('Price', 0.0):.2f}€"
            return f"{last['Time']} | {last['Category']} | {last['Payment']} | {last.get('Price', 0.0):.2f}€"
        return "No sales yet today."
    except Exception:
        return "Error reading file."

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
    df_cleaned = df_sales[~df_sales['Time'].str.contains("SUMMARY|TOTAL CARD|TOTAL CASH|GROSS TOTAL", na=False)].copy()
    math_only = df_cleaned[~df_cleaned['Time'].str.contains("TOTAL-", na=False)].copy()
    math_only.loc[:, 'Price'] = pd.to_numeric(math_only['Price'], errors='coerce')
    
    card_sum = round(math_only[math_only['Payment'] == 'Card']['Price'].sum(), 2)
    cash_sum = round(math_only[math_only['Payment'] == 'Cash']['Price'].sum(), 2)
    total_gross = round(card_sum + cash_sum, 2)

    summary_rows = [
        {"Time": "---SUMMARY---", "Category": "", "Payment": "", "Price": None},
        {"Time": "TOTAL CARD", "Category": "", "Payment": "", "Price": card_sum},
        {"Time": "TOTAL CASH", "Category": "", "Payment": "", "Price": cash_sum},
        {"Time": "GROSS TOTAL", "Category": "", "Payment": "", "Price": total_gross}
    ]
    df_final = pd.concat([df_cleaned, pd.DataFrame(summary_rows)], ignore_index=True)
    df_final.to_csv(full_path, index=False)

def view_daily_report(full_path):
    if not os.path.exists(full_path):
        print("\n>> Δεν υπάρχουν πωλήσεις.")
        return
    df = pd.read_csv(full_path)
    df_display = df[~df['Time'].str.contains("SUMMARY|TOTAL CARD|TOTAL CASH|GROSS TOTAL", na=False)].copy()
    
    print("\n" + "-"*65)
    print(f"ΑΝΑΛΥΤΙΚΗ ΚΑΤΑΣΤΑΣΗ ΠΩΛΗΣΕΩΝ - {datetime.now().strftime('%d/%m/%Y')}")
    print("-" * 65)
    
    if not df_display.empty:
        rows = df_display.to_dict('records')
        print(f"{'Time':<12} {'Category':<25} {'Payment':<10} {'Price':<10}")
        print("-" * 65)

        for row in rows:
            time_val = str(row['Time'])
            price_val = f"{float(row['Price']):.2f}€" if pd.notnull(row['Price']) else ""
            cat_text = str(row['Category'])
            
            if "REFUND" in cat_text:
                line = f"{time_val:<12} {cat_text:<25} {str(row['Payment']):<10} {price_val:<10}"
                print(f"{RED}{line}{RESET}")
            elif 'TOTAL-' in time_val:
                display_time = time_val.replace('TOTAL-', '')
                line = f"{display_time:<12} {cat_text:<25} {str(row['Payment']):<10} {price_val:<10}"
                print(f"{DARK_GREEN}{line}{RESET}")
            elif any(r['Time'] == f"TOTAL-{time_val}" for r in rows):
                line = f"{time_val:<12} {cat_text:<25} {str(row['Payment']):<10} {price_val:<10}"
                print(f"{BRIGHT_GREEN}{line}{RESET}")
            else:
                line = f"{time_val:<12} {cat_text:<25} {str(row['Payment']):<10} {price_val:<10}"
                print(line)

        math_only = df_display[~df_display['Time'].str.contains("TOTAL-", na=False)].copy()
        math_only.loc[:, 'Price'] = pd.to_numeric(math_only['Price'], errors='coerce')
        card_total = math_only[math_only['Payment'] == 'Card']['Price'].sum()
        cash_total = math_only[math_only['Payment'] == 'Cash']['Price'].sum()
        
        print("-" * 65)
        print(f"Σύνολο Κάρτας:   {card_total:10.2f}€")
        print(f"Σύνολο Μετρητών: {cash_total:10.2f}€")
        print(f"ΓΕΝΙΚΟ ΣΥΝΟΛΟ:   {card_total + cash_total:10.2f}€")
    else:
        print("Δεν βρέθηκαν πωλήσεις.")
    print("-" * 65)

def main_menu():
    now = datetime.now()
    full_path = get_current_path()
    categories = load_categories()
    last_sale_str = get_last_sale_info(full_path)
    
    clear_screen()
    print("="*45)
    print(f"   DEAL EMPORIO - POS SYSTEM")
    print(f"   Ημερομηνία: {now.strftime('%d/%m/%Y')}")
    print("="*45)
    print(f" LAST SALE: {last_sale_str}")
    print("="*45)
    print("[1] Νέα Πώληση")
    print("[2] Προβολή Σημερινών Πωλήσεων")
    print("[3] Διαγραφή τελευταίας σειράς")
    print("[4] Επιστροφή / Refund")
    print("[5] Έξοδος")
    
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
                if price <= 0:
                    print(">> Η τιμή πρέπει να είναι μεγαλύτερη από 0."); input("Enter..."); continue
                basket.append({"Category": category, "Price": price})
                running_total += price
            except ValueError:
                print(">> Σφάλμα (πληκτρολογήστε μόνο αριθμό)."); input("Enter..."); continue
            
            while True:
                cont = input(f"\nΠροσθήκη άλλου είδους; [y/n]: ").lower().strip()
                if cont in ['y', 'n']: break
                print("Παρακαλώ επιλέξτε 'y' ή 'n'.")
            if cont == 'n': break
        
        if not basket: return True
        payment = get_choice(["Card", "Cash"], f"Πληρωμή: {running_total:.2f}€")
        if payment == "BACK": return True

        timestamp = datetime.now().strftime("%H:%M:%S")
        new_entries = [{"Time": timestamp, "Category": i["Category"], "Payment": payment, "Price": i["Price"]} for i in basket]
        if len(basket) > 1:
            new_entries.append({"Time": f"TOTAL-{timestamp}", "Category": ">>> TOTAL", "Payment": payment, "Price": running_total})
        
        save_path = get_current_path()
        df_new = pd.DataFrame(new_entries)
        if os.path.exists(save_path):
            df_existing = pd.read_csv(save_path)
            df_cleaned_existing = df_existing[~df_existing['Time'].str.contains("SUMMARY|TOTAL CARD|TOTAL CASH|GROSS TOTAL", na=False)]
            df_final = pd.concat([df_cleaned_existing, df_new], ignore_index=True)
        else:
            df_final = df_new
        update_and_save(df_final, save_path)
        input("\nΟλοκληρώθηκε. Enter...")

    elif cmd == '2':
        view_daily_report(get_current_path())
        input("\nΠιέστε Enter...")

    elif cmd == '3':
        target_path = get_current_path()
        if os.path.exists(target_path):
            df = pd.read_csv(target_path)
            df_sales = df[~df['Time'].str.contains("SUMMARY|TOTAL CARD|TOTAL CASH|GROSS TOTAL", case=False, na=False)].copy()
            
            if not df_sales.empty:
                last_row = df_sales.iloc[-1]
                last_time = str(last_row['Time'])
                
                # --- CONFIRMATION DIALOG ---
                print(f"\n{RED}ΠΡΟΣΟΧΗ: Πρόκειται να διαγραφεί η τελευταία εγγραφή.{RESET}")
                confirm = input("Είστε σίγουροι; [y/n]: ").lower().strip()
                
                if confirm == 'y':
                    if "TOTAL-" in last_time:
                        original_timestamp = last_time.replace("TOTAL-", "")
                        df_sales = df_sales[df_sales['Time'] != original_timestamp]
                        df_sales = df_sales[df_sales['Time'] != last_time]
                        print(f"\n>> Διαγράφηκε η ομαδική πώληση ({original_timestamp}).")
                    else:
                        df_sales = df_sales[:-1]
                        print("\n>> Διαγράφηκε η τελευταία εγγραφή.")
                    update_and_save(df_sales, target_path)
                else:
                    print("\n>> Η διαγραφή ακυρώθηκε.")
            else: 
                print("\n>> Δεν υπάρχουν εγγραφές.")
        input("\nΠιέστε Enter...")

    elif cmd == '4':
        clear_screen()
        print("--- ΕΠΙΣΤΡΟΦΗ / REFUND ---")
        category = get_choice(categories, "Ποιο είδος επιστρέφεται;")
        if category == "BACK": return True
        try:
            price_input = input(f"Ποσό επιστροφής για {category}: ").strip()
            price = float(price_input)
            if price <= 0: 
                print(">> Εισάγετε θετικό αριθμό."); input("Enter..."); return True
            payment = get_choice(["Card", "Cash"], "Πώς θα γίνει η επιστροφή χρημάτων;")
            if payment == "BACK": return True

            timestamp = datetime.now().strftime("%H:%M:%S")
            new_entry = pd.DataFrame([{"Time": timestamp, "Category": f"REFUND: {category}", "Payment": payment, "Price": -price}])
            
            save_path = get_current_path()
            if os.path.exists(save_path):
                df_existing = pd.read_csv(save_path)
                df_cleaned_existing = df_existing[~df_existing['Time'].str.contains("SUMMARY|TOTAL CARD|TOTAL CASH|GROSS TOTAL", na=False)]
                df_final = pd.concat([df_cleaned_existing, new_entry], ignore_index=True)
            else:
                df_final = new_entry
            update_and_save(df_final, save_path)
            print(f"\n>> Επιστροφή {price:.2f}€ καταχωρήθηκε.")
            input("Enter...")
        except ValueError:
            print(">> Σφάλμα."); input("Enter...")

    elif cmd == '5':
        return False
    return True

if __name__ == "__main__":
    while main_menu():
        pass