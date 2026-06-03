import csv
import sys


def main():
    # Three command-line arguments
    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not input_file.endswith(".csv") or not output_file.endswith(".csv"):
        sys.exit("Not a CSV file")

    data = read_csv(input_file)
    write_csv(output_file, data)


def read_csv(file_name):
    try:
        result = []
        with open(file_name, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Split the name: "Last, First"
                last, first = [part.strip() for part in row['name'].split(',')]
                house = row['house']
                result.append({
                    "first": first,
                    "last": last,
                    "house": house
                })
        return result

    except FileNotFoundError:
        sys.exit("File does not exist")


def write_csv(file_name, data):
    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ["first", "last", "house"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow({
                "first": row["first"],
                "last": row["last"],
                "house": row["house"]
            })


if __name__ == "__main__":
    main()
