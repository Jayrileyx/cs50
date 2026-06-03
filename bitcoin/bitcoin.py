import requests
import sys


def main():
    try:
        if len(sys.argv) < 2:
            sys.exit("Missing command-line argument")
        user_input = sys.argv[1]
        if user_input.isalpha():
            sys.exit("Command-line argument is not a number")

        user_input = float(user_input)
        # Command-line argument rejects non positive integers
        if user_input > 0:
            # Query the API CoinCap Bitcoin Price Index
            response = requests.get(
                "https://rest.coincap.io/v3/assets/bitcoin?apiKey=799adffd3375d5c52200eb55a1c01cbb5fed2abe42c44027177c22baacb0f837"
            )
            response.raise_for_status()
    except requests.RequestException:
        print("Couldn't complete request!")
    except requests.HTTPError:
        print("Couldn't complete request!")

    # Return JSON
    content = response.json()
    data_obj = content.get("data", None)
    price_usd = data_obj.get("priceUsd")
    amount = float(price_usd) * user_input
    print(f"${amount:,.4f}")


main()
