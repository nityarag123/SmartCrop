"""Farmspace Flask application and CLI entrypoint."""
import os
import sqlite3
from datetime import datetime
from functools import wraps

import requests
from flask import Flask, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from model import predict_crop, train_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "farmspace.db")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-this-farmspace-secret")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_error=None):
    db = g.pop("db", None)
    if db:
        db.close()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please sign in to continue.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def init_db():
    db = sqlite3.connect(DATABASE)
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
          email TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL,
          created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS products (
          id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
          description TEXT NOT NULL, category TEXT NOT NULL,
          price REAL NOT NULL, icon TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS orders (
          id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
          total REAL NOT NULL, status TEXT NOT NULL DEFAULT 'Confirmed',
          created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS order_items (
          id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER NOT NULL,
          product_id INTEGER NOT NULL, product_name TEXT NOT NULL,
          price REAL NOT NULL, quantity INTEGER NOT NULL,
          FOREIGN KEY (order_id) REFERENCES orders(id)
        );
    """)
    if db.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
        db.executemany("INSERT INTO products (name, description, category, price, icon) VALUES (?, ?, ?, ?, ?)", [
            ("Neem Guard", "Organic neem-based pest control for vegetables.", "Pesticide", 349, "🌿"),
            ("Soil Boost NPK", "Balanced fertilizer for healthy roots and growth.", "Fertilizer", 599, "🌱"),
            ("Bio Fungus Care", "Protects crops from common fungal diseases.", "Pesticide", 425, "🛡️"),
            ("Compost Plus", "Nutrient-rich organic compost, 5 kg pack.", "Fertilizer", 299, "🪴"),
        ])
    db.commit()
    db.close()


def weather_for(location):
    key = os.getenv("OPENWEATHER_API_KEY")
    if key and location:
        try:
            data = requests.get("https://api.openweathermap.org/data/2.5/forecast", params={"q": location, "appid": key, "units": "metric"}, timeout=8).json()
            if data.get("cod") == "200":
                days = []
                for item in data["list"]:
                    if "12:00:00" in item["dt_txt"]:
                        days.append({"date": item["dt_txt"][:10], "temp": round(item["main"]["temp"]), "humidity": item["main"]["humidity"], "description": item["weather"][0]["description"].title()})
                return days[:5], False
        except requests.RequestException:
            pass
    return ([
        {"date": "Today", "temp": 29, "humidity": 66, "description": "Partly cloudy"},
        {"date": "Tomorrow", "temp": 30, "humidity": 61, "description": "Sunny intervals"},
        {"date": "Day 3", "temp": 28, "humidity": 70, "description": "Light rain"},
        {"date": "Day 4", "temp": 27, "humidity": 72, "description": "Cloudy"},
        {"date": "Day 5", "temp": 29, "humidity": 64, "description": "Clear"},
    ], True)


@app.context_processor
def cart_count():
    return {"cart_count": sum(session.get("cart", {}).values())}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name, email, password = request.form.get("name", "").strip(), request.form.get("email", "").strip().lower(), request.form.get("password", "")
        if not name or not email or len(password) < 6:
            flash("Enter your name, email, and a password of at least 6 characters.", "error")
        else:
            try:
                db = get_db()
                db.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)", (name, email, generate_password_hash(password)))
                db.commit()
                flash("Your Farmspace account is ready. Please sign in.", "success")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("An account already exists for that email.", "error")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = get_db().execute("SELECT * FROM users WHERE email = ?", (request.form.get("email", "").strip().lower(),)).fetchone()
        if user and check_password_hash(user["password_hash"], request.form.get("password", "")):
            session.clear(); session["user_id"] = user["id"]; session["user_name"] = user["name"]
            return redirect(url_for("recommend"))
        flash("Invalid email or password.", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear(); flash("You have been signed out.", "success")
    return redirect(url_for("home"))


@app.route("/recommend", methods=["GET", "POST"])
@login_required
def recommend():
    result = None
    if request.method == "POST":
        try:
            values = {key: float(request.form[key]) for key in ("temperature", "humidity", "rainfall", "ph", "nitrogen", "phosphorus", "potassium")}
            result = predict_crop(values)
        except (KeyError, ValueError):
            flash("Please enter valid numeric conditions.", "error")
    return render_template("recommend.html", result=result)


@app.route("/weather")
def weather():
    location = request.args.get("location", "")
    forecast, demo = weather_for(location)
    return render_template("weather.html", forecast=forecast, location=location, demo=demo)


@app.route("/shop")
def shop():
    return render_template("shop.html", products=get_db().execute("SELECT * FROM products ORDER BY category, name").fetchall())


@app.post("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    if not get_db().execute("SELECT id FROM products WHERE id = ?", (product_id,)).fetchone():
        return redirect(url_for("shop"))
    cart = session.get("cart", {}); key = str(product_id); cart[key] = cart.get(key, 0) + 1; session["cart"] = cart
    flash("Added to your cart.", "success")
    return redirect(request.referrer or url_for("shop"))


@app.route("/cart", methods=["GET", "POST"])
def cart():
    cart_data = session.get("cart", {})
    if request.method == "POST":
        for product_id in list(cart_data):
            quantity = max(0, int(request.form.get(f"qty_{product_id}", 0)))
            if quantity: cart_data[product_id] = quantity
            else: cart_data.pop(product_id)
        session["cart"] = cart_data
        return redirect(url_for("cart"))
    items, total = [], 0
    for product_id, quantity in cart_data.items():
        product = get_db().execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        if product:
            subtotal = product["price"] * quantity; items.append({"product": product, "quantity": quantity, "subtotal": subtotal}); total += subtotal
    return render_template("cart.html", items=items, total=total)


@app.post("/checkout")
@login_required
def checkout():
    cart_data = session.get("cart", {})
    if not cart_data:
        flash("Your cart is empty.", "error"); return redirect(url_for("shop"))
    db, items, total = get_db(), [], 0
    for product_id, quantity in cart_data.items():
        product = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        if product: items.append((product, quantity)); total += product["price"] * quantity
    cursor = db.execute("INSERT INTO orders (user_id, total) VALUES (?, ?)", (session["user_id"], total))
    for product, quantity in items:
        db.execute("INSERT INTO order_items (order_id, product_id, product_name, price, quantity) VALUES (?, ?, ?, ?, ?)", (cursor.lastrowid, product["id"], product["name"], product["price"], quantity))
    db.commit(); session["cart"] = {}
    flash("Order confirmed. Thank you for shopping with Farmspace!", "success")
    return redirect(url_for("orders"))


@app.route("/orders")
@login_required
def orders():
    db = get_db(); orders = db.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY id DESC", (session["user_id"],)).fetchall()
    return render_template("orders.html", orders=orders)


@app.route("/orders/<int:order_id>")
@login_required
def order_detail(order_id):
    db = get_db(); order = db.execute("SELECT * FROM orders WHERE id = ? AND user_id = ?", (order_id, session["user_id"])).fetchone()
    if not order: return redirect(url_for("orders"))
    return render_template("order_detail.html", order=order, items=db.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,)).fetchall())


# Initialize the SQLite schema for both ``python main.py`` and WSGI servers.
init_db()

if __name__ == "__main__":
    train_model()
    app.run(debug=True)
