import os

# This line finds the exact folder where this script (sort_categories.py) is saved
script_dir = os.path.dirname(os.path.abspath(__file__))
# This joins that folder path with your filename
filename = os.path.join(script_dir, 'categories.txt')

try:
    # 1. Read and process the data
    with open(filename, 'r', encoding='utf-8') as file:
        lines = []
        for line in file:
            clean_line = line.strip()
            if clean_line:
                # [cite_start]Remove the tag found in your file [cite: 1]
                clean_line = clean_line.replace('', '').strip()
                lines.append(clean_line)

    # 2. Sort the items alphabetically
    lines.sort()

    # 3. Overwrite the original file
    with open(filename, 'w', encoding='utf-8') as file:
        for item in lines:
            file.write(item + '\n')

    print(f"Success! {filename} has been updated.")

except FileNotFoundError:
    print(f"Still can't find it. The script looked here: {filename}")