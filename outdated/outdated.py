MONTH = {
            "January" : "01",
            "February" : "02",
            "March" : "03",
            "April" : "04",
            "May" : "05",
            "June" : "06",
            "July" : "07",
            "August" : "08",
            "September" : "09",
            "October" : "10",
            "November" : "11",
            "December" : "12"
        }

def main():
    while True:
        try:
            date = input("Date: ").strip()

            # Format: Month, Day, Year
            if "," in date:
                month_str, rest = date.split(" ", 1)
                day_str, year = rest.replace(",", "").split()
                month = MONTH[month_str]
                day = int(day_str)
                year = int(year)

                if not (1 <= day <= 31):
                    continue

            else:
                month, day, year = date.split('/')
                month = int(month)
                day = int(day)
                year = int(year)

                # Prompt for valid date
                if not (1 <= month <= 12 and 1 <= day <= 31):
                    continue

                month = f"{month:02}"

            print(f"{year}-{month}-{day:02}")
            break

        except(ValueError, KeyError):
            continue

main()
