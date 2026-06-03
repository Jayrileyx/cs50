import random


def main():
    level = get_level()
    score = 0

    for _ in range(10):
        x = generate_integer(level)
        y = generate_integer(level)

        tries = 0
        while tries < 3:
            try:
                print(f"{x} + {y} = ", end="")
                answer = int(input())
                if answer == x + y:
                    score += 1
                    break
                # Output EEE if incorrect
                else:
                    # Try three guesses and then show answer
                    print("EEE")
                    tries += 1
            except ValueError:
                print("EEE")
                tries += 1

            if tries == 3:
                print(f"{x} + {y} = {x + y}")

    # Output score = number of correct answers out of 10
    print(f"Score: {score}")


def get_level():
    # Prompt user for level between 1 and 3
    while True:
        try:
            level = int(input("Level: "))
            if 1 <= level <= 3:
                return level
        except ValueError:
            continue


def generate_integer(level):
    # Randomly generate 10 math problems formatted as X + Y =
    if level == 1:
        return random.randint(0, 9)
    elif level == 2:
        return random.randint(10, 99)
    elif level == 3:
        return random.randint(100, 999)
    else:
        raise ValueError("Invalid level")


if __name__ == "__main__":
    main()
