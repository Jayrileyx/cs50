import re

def main():
    ip = input("IPv4 Address: ")
    if validate(ip):
        print("Valid")
    else:
        print("Invalid")

def validate(ip):
    pattern = r'^((25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})\.){3}(25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})$'
    return re.match(pattern, ip) is not None

if __name__ == "__main__":
    main()
