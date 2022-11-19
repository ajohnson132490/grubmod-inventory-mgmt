import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///inventory.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords must match", 400)

        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))

        # Make sure username is unique
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Insert data into database
        if not rows:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password)
        else:
            return apology("Username must be unique", 400)

        # Redirect to the login page
        return redirect("/")

    else:
        return render_template("register.html")


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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


@app.route("/")
@login_required
def index():
    recentTransactions = db.execute("SELECT * from transactions WHERE username=? ORDER BY time DESC LIMIT 20", session["user_id"])
    currentCash = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])
    totalValue = db.execute("SELECT SUM(price) FROM merchandise WHERE username=?", session["user_id"])
    if totalValue[0]['SUM(price)'] != None:
        return render_template("index.html",
        recentTransactions=recentTransactions, currentCash=currentCash, totalValue=totalValue[0]['SUM(price)']*-1)
    else:
        return render_template("index.html",
        recentTransactions=recentTransactions, currentCash=currentCash, totalValue=0)

@app.route("/inventory", methods=["GET", "POST"])
@login_required
def inventory():
    if request.method == "POST":
        """Display current inventory"""
        if not request.form.get("sort"):
                currentInventory = db.execute("SELECT * from merchandise WHERE username=? ORDER BY ?", session["user_id"], "id")
                return render_template("inventory.html", merchandise=currentInventory)
        else:
            sortBy = request.form.get("sort")
            currentInventory = db.execute(f"SELECT * from merchandise WHERE username=? ORDER BY {sortBy}", session["user_id"])
            return render_template("inventory.html", merchandise=currentInventory)
    """Display current inventory"""
    currentInventory = db.execute("SELECT * from merchandise WHERE username=?", session["user_id"])
    return render_template("inventory.html", merchandise=currentInventory)


@app.route("/sale", methods=["GET", "POST"])
@login_required
def sale():
    """Sell an item from the inventory"""

    if request.method == "POST":
        # Make sure the request is valid
        if not request.form.get("unitId"):
            return apology("Must have a unit id", 403)
        elif not db.execute("SELECT * FROM merchandise WHERE id=? AND username=?", request.form.get("unitId"), session["user_id"]):
            return apology("This unit does not exist", 404)

        if float(request.form.get("price")) <= 0:
            return apology("Please don't just give stuff away", 403)

        # Remove item from merchandise
        db.execute("DELETE FROM merchandise WHERE id=? AND username=?", request.form.get("unitId"), session["user_id"])

        # If request is valid, add it as a transaction
        if not request.form.get("market"):
            db.execute("INSERT INTO transactions (unitId, value, username) VALUES (?, ?, ?)",
            request.form.get("unitId"), float(request.form.get("price")), session["user_id"])
        else:
            db.execute("INSERT INTO transactions (unitId, value, market, username) VALUES (?, ?, ?, ?)",
            request.form.get("unitId"), float(request.form.get("price")), request.form.get("market"), session["user_id"])

        # Add cash to balance
        fundsAvailable = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
        float(fundsAvailable[0]['cash']) + float(request.form.get("price")), session["user_id"])

        return redirect("/")

    else:
        return render_template("sale.html")


@app.route("/purchase", methods=["GET", "POST"])
@login_required
def purchase():
    """Add an item to inventory"""

    # Adding an item to the mechandise table
    if request.method == "POST":
        # Make sure all the data is valid
        if not float(request.form.get("price")) >= 1:
            return apology("Must enter amount paid for item", 400)

        if not request.form.get("condition"):
            return apology("Must select a condition", 400)

        fundsAvailable = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
        if float(fundsAvailable[0]['cash']) < float(request.form.get("price")):
            return apology("You're too broke to buy this", 403)


        # Add the item to current merchandise
        db.execute("INSERT INTO merchandise (type, price, condition, username) VALUES (?, ?, ?, ?)",
        request.form.get("type"), -1 * float(request.form.get("price")), request.form.get("condition"), session["user_id"])

        # Get the unit id
        unitID = db.execute("SELECT id FROM merchandise WHERE username=? ORDER BY id DESC LIMIT 0,1", session["user_id"])

        # Add the transaction to the transaction table
        # If no marketplace specified
        if not request.form.get("market"):
            db.execute("INSERT INTO transactions (unitId, value, username) VALUES (?, ?, ?)",
            unitID[0]["id"], -1 * float(request.form.get("price")), session["user_id"])
        else:
            # If marketplace is specified
            db.execute("INSERT INTO transactions (unitId, value, market, username) VALUES (?, ?, ?, ?)",
            unitID[0]["id"], -1 * float(request.form.get("price")), request.form.get("market"), session["user_id"])

        # Remove cash from balance
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
        float(fundsAvailable[0]['cash']) - float(request.form.get("price")), session["user_id"])

        return redirect("/")
    else:
        conditions = ["Excellent", "Good", "Acceptable", "Poor", "For Parts"]
        return render_template("purchase.html", conditions=conditions)