from cs50 import get_string

text = get_string("Text: ")

# Calculate letters, words, sentences in text
letters = 0
space = 0
sentences = 0

for char in text:
    # Check if alphabetical
    if char.isalpha():
        letters += 1
    elif char == ' ':
        space += 1
    elif char == '.' or char == '?' or char == '!':
        sentences += 1

words = space + 1

L = (letters / words) * 100
S = (sentences / words) * 100

# Calculate Coleman-Liau formula (round)
grade = round(0.0588 * L - 0.296 * S - 15.8)

# Print grade level unless above 16 or before grade 1
if grade > 16:
    print("Grade 16+")
elif grade < 1:
    print("Before Grade 1:")
else:
    print(f"Grade {grade}")
