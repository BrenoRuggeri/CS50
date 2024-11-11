import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

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

    stocks = db.execute("SELECT symbol, SUM(shares) AS total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
                        user_id=session["user_id"])

    cash = db.execute("SELECT cash from users WHERE id = :user_id",
                      user_id=session["user_id"])[0]["cash"]

    total_value = cash
    grand_total = cash

    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["price"] = quote["price"]
        stock["value"] = stock["price"] * stock["total_shares"]
        total_value += stock["value"]
        grand_total += stock["value"]

    return render_template("index.html", stocks=stocks, cash=cash, total_value=total_value, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        if not symbol:
            return apology("Must give a symbol")

        elif not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Must provide a positive integer of shares")

        quote = lookup(symbol)
        if quote is None:
            return apology("Must provide a symbol")

        price = quote["price"]
        transaction_cost = int(shares) * price
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id",
                          user_id=session["user_id"])[0]["cash"]

        # Check if user money is greater than transactions cost
        if cash < transaction_cost:
            return apology("You don't have enough money")

        # Update user_cash from database after transactions
        db.execute("UPDATE users SET cash = cash - :transaction_cost WHERE id = :user_id",
                   transaction_cost=transaction_cost, user_id=session["user_id"])

        # Update transactions table
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                   user_id=session["user_id"], symbol=symbol, shares=shares, price=price)

        flash(f"Bought!")

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id= :user_id ORDER BY date DESC", user_id=session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/deposit_cash", methods=["GET", "POST"])
@login_required
def deposit_cash():
    """Deposit Cash"""
    if request.method == "GET":
        return render_template("deposit.html")

    else:
        new_cash = int(request.form.get("new_cash"))

        if not new_cash:
            return apology("Put how much money you want deposit")

        user_id = session["user_id"]

        # Update cash of user
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
        user_cash = user_cash_db[0]["cash"]

        # Update user_cash from database before transactions
        update_cash = user_cash + new_cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", update_cash, user_id)

        return redirect("/")


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
            return apology("Invalid Symbol")
        return render_template("quote.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()

    # Register user
    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Must provide Username")

        if not password:
            return apology("Must provide Password")

        if not confirmation:
            return apology("You must confirm your password")

        if password != confirmation:
            return apology("Do not Match")

        # Store user password into hash
        hash = generate_password_hash(password, method='scrypt', salt_length=16)

        try:
            # Insert new users into database
            new_user = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        except:
            return apology("User already exists")

        # Remember which user has logged in
        session["user_id"] = new_user

        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        symbols_user = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = :id GROUP BY symbol HAVING SUM(shares) > 0", id=user_id)
        symbols = [row["symbol"] for row in symbols_user]

        return render_template("sell.html", symbols=symbols)

    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("Must give a symbol")

        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Must provide a positive integer of shares")

        shares = int(shares)
        stock = lookup(symbol.upper())

        if stock == None:
            return apology("Symbol doesn't exist")

        transaction_cost = shares * stock["price"]
        user_id = session["user_id"]

        user_cash_db = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
        user_cash = user_cash_db[0]["cash"]

        user_shares = db.execute(
            "SELECT SUM(shares) AS total_shares FROM transactions WHERE user_id = :id AND symbol = :symbol GROUP BY symbol", id=user_id, symbol=symbol)
        user_shares_real = user_shares[0]["total_shares"]

        if shares > user_shares_real:
            return apology("Not enough shares")

        update_cash = user_cash + transaction_cost
        db.execute("UPDATE users SET cash = ? WHERE id = ?", update_cash, user_id)

        date = datetime.datetime.now()

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                   user_id, stock["symbol"], -shares, stock["price"], date)

        flash("Sold!")

        return redirect("/")
