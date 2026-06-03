from cs50 import get_float

while True:
    change = get_float("What is the change needed?")
    if (change > 0):
        break

# Change into cents first to avoid floating-point imprescision
total = int(change * 100)

# Calculate each set of coins
quarters = int(total / 25)
total -= quarters * 25

dimes = int(total / 10)
total -= dimes * 10

nickels = int(total / 5)
total -= nickels * 5

pennies = total

# Sum of the total
total_coins = quarters + dimes + nickels + pennies

print(total_coins)
