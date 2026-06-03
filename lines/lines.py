import sys


def main():
    count = 0
    # Two command-line arguments
    if len(sys.argv) < 2:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 2:
        sys.exit("Too many command-line arguments")
    # Count the lines of code only while checking for .py
    else:
        file_name = sys.argv[1]
        if file_name.endswith(".py"):
            try:
                with open(file_name) as file:
                    for line in file:
                        if not line.lstrip().startswith("#") and line.split() != []:
                            count += 1
            except FileNotFoundError:
                sys.exit("File does not exist")
        else:
            sys.exit("Not a Python file")

    print(count)


main()
