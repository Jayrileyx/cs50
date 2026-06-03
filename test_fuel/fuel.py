def main():
    percent = convert(input("Fraction: "))
    print(gauge(percent))

def convert(fraction):
    while True:
        try:
            n = fraction.find("/")
            num = int(fraction[0:n])
            den = int(fraction[n+1:])

            if num/den <= 1:
                percent = round(num/den * 100)
                return percent
            else:
                fraction = input("Fraction: ")
                pass
        except (ZeroDivisionError, ValueError):
            raise


def gauge(percent):
    if percent >= 99:
        return "F"
    elif percent <= 1:
        return "E"
    else:
        return (str(percent) + "%")


if __name__ == "__main__":
    main()




