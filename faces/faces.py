def main():
    user_text = input("Please provide input with emoticon. ")
    replacement_smiling = "🙂"
    replacement_frowning = "🙁"
    if (":)" in user_text):
        user_text = user_text.replace(":)", replacement_smiling)
    if (":(" in user_text):
        user_text = user_text.replace(":(", replacement_frowning)

    print(user_text)


main()
