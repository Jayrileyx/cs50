def main():
    try:
        grocery_list = {}
        while True:
            item = input().strip().upper()
            # Calculate how many items of each
            if item:
                grocery_list[item] = grocery_list.get(item, 0) + 1
    except EOFError:
        # List needs to be sorted
        for item in sorted(grocery_list):
            print(f"{grocery_list[item]} {item}")

main()
