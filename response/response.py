import validators


email = input("What's your email? ").strip()

if validators.email(email):
    print("Valid")
else:
    print("Invalid")
