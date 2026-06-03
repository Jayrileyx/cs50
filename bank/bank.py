greeting = input("Greeting: ").strip().lower()

# Handles anything starting with hello
if greeting.startswith("hello"):
    print("$0")
# Handles anything that starts with h
elif greeting.startswith("h"):
    print("$20")
else:
    print("$100")
