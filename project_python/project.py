def main():
    balance = 0.0

    print("Welcome to Simple Bank App")

    while True:
        action = input("Choose: deposit, withdraw, check balance, quit: ").strip().lower()

        if action == "deposit":
            amount = float(input("Enter amount: "))
            balance = deposit(balance, amount)
            print(f"New balance: ${balance:.2f}")

        elif action == "withdraw":
            amount = float(input("Enter amount: "))
            balance = withdraw(balance, amount)
            print(f"New balance: ${balance:.2f}")

        elif action == "check balance":
            print(f"Current balance: ${check_balance(balance):.2f}")

        elif action == "quit":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")

def deposit(balance, amount):
    if amount < 0:
        raise ValueError("Cannot deposit negative amount")
    return balance + amount

def withdraw(balance, amount):
    if amount < 0:
        raise ValueError("Insufficient funds")
    if amount > balance:
        return balance
    return balance - amount

def check_balance(balance):
    return balance

if __name__ == "__main__":
    main()
