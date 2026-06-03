def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    # Start with two letters
    if not s[0:2].isalpha():
        return False

    # Plate must range between two and six characters
    if (len(s)) < 2 or (len(s)) > 6:
        return False

    # Numbers cannot be at index point before a letter
    for i in range(len(s) - 1):
        if s[i].isdigit() and s[i + 1].isalpha():
            return False

    # Check if first digit is "0"
    for i in range(len(s)):
        if s[i].isdigit():
            if s[i] == "0":
                return False
            break

    # No periods, punctuation or spaces
    for i in range(len(s)):
        if s[i] == "." or s[i] == "!" or s[i] == "?" or s[i].isspace():
            return False

    else:
        return True


main()
