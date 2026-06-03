import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    # Users stocks and shares
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    total_value = 0

    stocks = db.execute("""
        SELECT symbol, SUM(shares) AS total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, user_id)

    # Add price and total value
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["value"] = quote["price"] * stock["total_shares"]
        total_value += stock["value"]

        # Format stock
        stock["price"] = f"${stock['price']:,.2f}"
        stock["value"] = f"${stock['value']:,.2f}"

    grand_total = total_value + cash

    # Format cash
    cash = f"${cash:,.2f}"
    total_value = f"${total_value:,.2f}"
    grand_total = f"${grand_total:,.2f}"

    return render_template("index.html", stocks=stocks, cash=cash, total_value=total_value, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")
        if not symbol:
            return apology("Must provide symbol")
        elif not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Must provide positive number")

        quote = lookup(symbol)
        if quote is None:
            return apology("Symbol not found")

        price = quote["price"]
        cost_share = int(shares) * price
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        if cash < cost_share:
            return apology("You do not have enough funds to purchase")

        # Update the table
        db.execute("UPDATE users SET cash = cash - :cost_share WHERE id = :user_id",
                   cost_share=cost_share, user_id=session["user_id"])

        # Add the purchase
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], symbol, shares, price)

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Query database for user's transactions, ordered by most recent
    user_id = session["user_id"]
    transactions = db.execute("""
        SELECT symbol, shares, price,
               CASE WHEN shares > 0 THEN 'BUY' ELSE 'SELL' END AS type,
               timestamp
        FROM transactions
        WHERE user_id = ?
        ORDER BY timestamp DESC
    """, user_id)

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        if not quote:
            return apology("Invaild symbol", 400)
        return render_template("quote.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Clear the user_id
    session.clear()

    # User route via POST
    if request.method == "POST":

        # Username was submitted
        if not request.form.get("username"):
            return apology("Must provide username.", 400)

        # Password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password.", 400)

        # Password confirmation
        elif not request.form.get("confirmation"):
            return apology("Must confirm password.", 400)

        # Password confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match.", 400)

        # Create query for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Check username does not exist
        if len(rows) != 0:
            return apology("Username already exists.", 400)

        # Insert new user into the database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                   request.form.get("username"), generate_password_hash(request.form.get("password")))

        # Create query for new user
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Remember the user
        session["user_id"] = rows[0]["id"]

        # Redirect user to homepage
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    user_id = session["user_id"]

    """Sell shares of stock"""
    # User stocks
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])

    # Submitted the form
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")
        if not symbol:
            return apology("Must provide a symbol")
        elif not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Must provide a positive integer")

        shares = int(shares)

        # Get total number of stocks
        rows = db.execute("""
            SELECT SUM(shares) AS total_shares
            FROM transactions
            WHERE user_id = ? AND symbol = ?
            """, session["user_id"], symbol)

        owned = rows[0]["total_shares"]

        if owned is None or owned < shares:
            return apology("Not enough shares")

        # Lookup stock price
        quote = lookup(symbol)
        if quote is None:
            return apology("Invalid stock")

        price = quote["price"]
        total_sale = shares * price

        # Update user's cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_sale, user_id)

        # Record sale (as negative shares)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, symbol, -shares, price)

        return redirect("/")

    else:
        # Show only symbols the user owns with shares > 0
        stocks = db.execute("""
            SELECT symbol, SUM(shares) AS total_shares
            FROM transactions
            WHERE user_id = ?
            GROUP BY symbol
            HAVING total_shares > 0
        """, user_id)

        return render_template("sell.html", stocks=stocks)


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    if request.method == "POST":
        # Get cash amount from form
        cash_to_add = request.form.get("cash")

        # Validate input
        if not cash_to_add:
            return apology("Must provide amount")
        try:
            cash_to_add = float(cash_to_add)
        except ValueError:
            return apology("Invalid amount")

        if cash_to_add <= 0:
            return apology("Amount must be positive")

        # Update user's cash balance
        user_id = session["user_id"]
        db.execute("UPDATE users SET cash = cash + :cash WHERE id = :user_id",
                   cash=cash_to_add, user_id=user_id)

        flash(f"Successfully added ${cash_to_add:.2f} to your account.")
        return redirect("/")

    else:
        return render_template("add_cash.html")
