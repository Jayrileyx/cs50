def main():
    word = input("Input: ")
    print("Output: ", shorten(word))


def shorten(word):
    vowels = "aeiouAEIOU"
    return "".join(c for c in word if c not in vowels)


if  __name__ == "__main__":
    main()
