def main():
    try:
        plate = input("Plate: ")
    except EOFError:
        return

    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    # Reject non-strings immediately
    if not isinstance(s, str):
        return False

    # Plate must be 2–6 characters
    if len(s) < 2 or len(s) > 6:
        return False

    # First two characters must be letters
    if not s[0].isalpha() or not s[1].isalpha():
        return False

    # Once numbers start, letters cannot appear after
    for i in range(len(s) - 1):
        if s[i].isdigit() and s[i + 1].isalpha():
            return False

    # First number cannot be zero
    for c in s:
        if c.isdigit():
            if c == "0":
                return False
            break

    # Only letters and numbers allowed
    for c in s:
        if not c.isalnum():
            return False

    return True



if __name__ == "__main__":
    main()
