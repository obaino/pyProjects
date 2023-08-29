# https://cs50.harvard.edu/python/2022/psets/6/pizza/

from sys import argv, exit
from tabulate import tabulate
import csv

def main():
    print(tabulate(get_books(), headers="keys", tablefmt="grid"))

def get_books():
    try:
        if len(argv) < 2:
            exit("Too few command-line arguments")
        elif len(argv) > 2:
            exit("Too many command-line arguments")
        else:
            with open(argv[1], "r") as file:
                if not argv[1].endswith(".csv"):
                    exit("Not a CSV file")
                else:
                    books_list = []
                    reader = csv.DictReader(file)
                    # get the first row of csv as keys
                    key_1, key_2, key_3, key_4, key_5 = reader.fieldnames
                    for row in reader:
                        books_list.append({key_2: row[key_2], key_3: row[key_3], key_4: row[key_4]})
                    return books_list

    except FileNotFoundError:
        exit("File does not exist")

if __name__ == "__main__":
    main()