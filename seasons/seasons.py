from datetime import date
import sys
import inflect

p = inflect.engine()


def main():
    try:
        year, month, day = [int(x) for x in input("Date of Birth: ").split("-")]
    except Exception:
        sys.exit("Invalid date")

    dob = birth_date(year, month, day)
    minutes = calculate_minutes(dob)
    words = p.number_to_words(minutes, andword="")
    print(words.capitalize() + " minutes")


def birth_date(year, month, day):
    try:
        dob = date(year, month, day)
    except ValueError:
        return "Invalid Date"
    return dob


def calculate_minutes(dob):
    return str(((date.today() - dob).days) * 24 * 60)

if __name__ == "__main__":
    main()

