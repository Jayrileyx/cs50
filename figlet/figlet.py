import sys
import pyfiglet
import random

figlet = pyfiglet.Figlet()
fonts = figlet.getFonts()

# Zero for random font
if len(sys.argv) == 1:
    chosen_font = random.choice(fonts)
    # Prompt user for str
    user_input = input("Input: ")
    # Output the text in desired font
    print(pyfiglet.figlet_format(user_input, font=chosen_font))

# Two for specific font (-f or --font)
elif len(sys.argv) == 3 and sys.argv[1] in ["-f", "--font"]:
    chosen_font = sys.argv[2]
    if chosen_font not in fonts:
        sys.exit("Invalid usage")
    user_input = input("Input: ")
    # Output the text in desired font
    print(pyfiglet.figlet_format(user_input, font=chosen_font))

# if not -f or --font
else:
    sys.exit("Invalid usage")
