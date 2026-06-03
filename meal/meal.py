def main():
    time_answer = input("What time is it? ")
    time = convert(time_answer)

    if time >= 7.0 and time <= 8.0:
        print("breakfast time")
    elif time >= 12.0 and time <= 13.0:
        print("lunch time")
    elif time >= 18.0 and time <= 19.0:
        print("dinner time")
    else:
        exit()


def convert(time_answer):
    # Split the time and minutes
    hours, minutes = time_answer.split(":")
    hours = int(hours)
    minutes = int(minutes)

    # Converts to decimal hours
    return hours + minutes / 60


if __name__ == "__main__":
    main()
