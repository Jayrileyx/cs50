import re


def main():
    s = input("Hours: ")
    print(convert(s))


def convert(s):
    # Require space before AM/PM
    pattern = r'^\s*(\d{1,2}(?::\d{2})?) (AM|PM) to (\d{1,2}(?::\d{2})?) (AM|PM)\s*$'
    match = re.match(pattern, s)

    if not match:
        raise ValueError("Invalid format")

    start_time, start_period, end_time, end_period = match.groups()

    start_24 = to_24_hour(start_time, start_period)
    end_24 = to_24_hour(end_time, end_period)

    return f"{start_24} to {end_24}"


def to_24_hour(time_str, period):
    if ':' in time_str:
        hours, minutes = map(int, time_str.split(':'))
    else:
        hours = int(time_str)
        minutes = 0

    if hours > 12 or minutes > 59:
        raise ValueError("Invalid time values")

    if period == "AM":
        if hours == 12:
            hours = 0
    elif period == "PM":
        if hours != 12:
            hours += 12

    return f"{hours:02}:{minutes:02}"


if __name__ == "__main__":
    main()
