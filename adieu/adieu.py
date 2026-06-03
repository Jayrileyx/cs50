import inflect

p = inflect.engine()
names = []

try:
    while True:
        names.append(input())
except EOFError:
    print(f"Adieu, adieu, to {p.join(names)}")
