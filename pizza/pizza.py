import csv
import sys
from tabulate import tabulate


def main():
    count = 0
    # Two command-line arguments
    if len(sys.argv) < 2:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 2:
        sys.exit("Too many command-line arguments")

    file_name = sys.argv[1]

    if not file_name.endswith(".csv"):
        sys.exit("Not a CSV file")

    headers, rows = read_csv(file_name)
    print(tabulate(rows, headers=headers, tablefmt="grid"))


def read_csv(file_path):
    try:
        with open(file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            headers = next(csv_reader)
            rows = list(csv_reader)
        return headers, rows
    except FileNotFoundError:
        sys.exit("File does not exist")


if __name__ == "__main__":
    main()
