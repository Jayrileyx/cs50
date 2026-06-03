def main():
    # Prompt user for fraction string
    while True:
        fraction = input("Fraction: ")
        try:
            result_float = calculate_fraction(fraction)
        except ValueError:
            continue
        except ZeroDivisionError:
            continue

        percentage = round(result_float * 100)

        if percentage <= 1:
            print("E")
        elif percentage >= 99:
            print("F")
        else:
            print(f"{percentage}%")
        break # Only exit after successful input


def calculate_fraction(fraction):
    # Split fraction string
    numerator_str, denominator_str = fraction.split('/')
    # Calculate fraction
    numerator = int(numerator_str)
    denominator = int(denominator_str)
    if denominator == 0:
        raise ZeroDivisionError("Please provide a non zero fraction.")
    elif not isinstance(numerator, int) or numerator < 0 or numerator > denominator:
        raise ValueError("Please provide a fraction.")

    return numerator / denominator


main()
