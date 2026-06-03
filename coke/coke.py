def main():
    amount_due = 50
    print("Amount Due: 50")
    # Loop through until amount is > 0
    while amount_due > 0:
        coin = int(input("Insert Coin: "))
        amount_due = calculate_amount_due(coin, amount_due)


def calculate_amount_due(coin, amount_due):
    # Check if the coin is accepted
    if coin == 25 or coin == 10 or coin == 5:
        amount_due -= coin
        if amount_due <= 0:
            print("Change Owed:", abs(amount_due))
            return amount_due

        # Calculate the amount due from each insert
        elif coin == 25:
            print("Amount Due:", amount_due)
        elif coin == 10:
            print("Amount Due:", amount_due)
        elif coin == 5:
            print("Amount Due:", amount_due)
    else:
        print("Amount Due:", amount_due)

    return amount_due


main()
