import emoji

str_emoji = input("Input: ")
output = emoji.emojize(str_emoji, language='alias')
print(f"Output: {output}")
