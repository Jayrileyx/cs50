import re


def main():
    s = input("HTML: ")
    result = parse(s)
    if result:
        print(result)


def parse(s):
    # ONLY match if it's inside src="..." in an iframe
    match = re.search(
        r'<iframe[^>]*src="https?://(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)"', s)
    if match:
        video_id = match.group(1)
        return f"https://youtu.be/{video_id}"
    return None


if __name__ == "__main__":
    main()
