filename = 'categories.txt'

try:
    # 1. Read and process the data
    with open(filename, 'r', encoding='utf-8') as file:
        lines = []
        for line in file:
            clean_line = line.strip()
            if clean_line:
                # Remove the tag found in the original list 
                clean_line = clean_line.replace('', '').strip()
                lines.append(clean_line)

    # 2. Sort the items alphabetically
    lines.sort()

    # 3. Overwrite the original file with the sorted content
    with open(filename, 'w', encoding='utf-8') as file:
        for item in lines:
            file.write(item + '\n')

    print(f"Done! '{filename}' has been updated and sorted alphabetically.")

except FileNotFoundError:
    print(f"Error: The file '{filename}' was not found in this folder.")