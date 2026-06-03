# Input from user
expression = input("Expression: ")

x, y, z = expression.split(" ")
x = float(x)
z = float(z)

# Assign each operator
if y == "+":
    result = x + z
elif y == "-":
    result = x - z
elif y == "*":
    result = x * z
elif y == "/":
    result = x / z
else:
    exit()

print(f"{result:.1f}")
