import os
import sys
from PIL import Image, ImageOps


def main():
    # Make sure to get two command-line arguments
    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check the file is not jpeg or png
    _, input_ext = os.path.splitext(input_file)
    _, output_ext = os.path.splitext(output_file)

    valid_exts = [".jpg", ".jpeg", ".png"]

    if input_ext.lower() not in valid_exts:
        sys.exit("Invalid input")
    elif output_ext.lower() not in valid_exts:
        sys.exit("Invalid input")
    # Input name matches output name
    elif input_ext.lower() != output_ext.lower():
        sys.exit("Input and output have different extensions")

    fix_image(input_file, output_file)


def fix_image(input_file, output_file):
    try:
        with Image.open(input_file) as photo:
            with Image.open("shirt.png") as shirt:
                size = shirt.size
                photo = ImageOps.fit(photo, size)
                photo.paste(shirt, shirt)
                photo.save(output_file)
    except FileNotFoundError:
        sys.exit("Input does not exist")


if __name__ == "__main__":
    main()
