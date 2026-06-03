def main():
    greeting = input("Greeting: ").strip().lower()
    greeting_value = value(greeting)
    if greeting_value == 0:
        print("$0")
    elif greeting_value == 20:
        print("$20")
    else:
        print("$100")


def value(greeting):
    if greeting.startswith("hello"):
        return 0
    elif greeting.startswith("h"):
        return 20
    else:
        return 100


if __name__ == "__main__":
    main()
