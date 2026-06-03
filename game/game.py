import random

# Infinite prompt of the level until positive integer
while True:
    try:
        level = int(input("Level: "))
        if level > 0:
            break
    except ValueError:
        continue

user_guess = random.randint(1, level)

# Prompt for guess
while True:
    try:
        guess = int(input("Guess: "))
        # Guess less than zero creates another prompt
        if guess < 1:
            continue
        if guess > level:
            print("Too large!")
            continue
        if guess < user_guess:
            print("Too small!")
        elif guess > user_guess:
            print("Too large!")
        else:
            print("Just right!")
            break
    # Accept values that do not fall in the range
    except ValueError:
        continue
