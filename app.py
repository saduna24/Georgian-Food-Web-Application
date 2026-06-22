from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

ADMIN_USER = "admin"
ADMIN_PASS = "password123"
DATABASE = "food.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Food(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Image TEXT,
            Description TEXT,
            Price REAL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Orders(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Total REAL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db()
    foods = conn.execute("SELECT * FROM Food").fetchall()
    cart = session.get("cart", {})
    cart_items = []
    total = 0

    for fid, qty in cart.items():
        food = conn.execute("SELECT * FROM Food WHERE Id=?", (fid,)).fetchone()
        if food:
            subtotal = food["Price"] * qty
            total += subtotal
            cart_items.append({
                "id": food["Id"],
                "name": food["Name"],
                "qty": qty,
                "price": food["Price"],
                "subtotal": subtotal
            })

    conn.close()
    return render_template("index.html", foods=foods, cart_items=cart_items, total=total)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_input = request.form.get("username")
        pass_input = request.form.get("password")
        
        if user_input == ADMIN_USER and pass_input == ADMIN_PASS:
            session["admin"] = True
            return redirect(url_for("index"))
            
        flash("Invalid username or password!")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/add/<int:id>")
def add(id):
    cart = session.get("cart", {})
    cart[str(id)] = cart.get(str(id), 0) + 1
    session["cart"] = cart
    return ("OK", 200)


@app.route("/remove/<int:id>")
def remove(id):
    cart = session.get("cart", {})
    cart.pop(str(id), None)
    session["cart"] = cart
    return redirect(url_for("index"))


@app.route("/product/create", methods=["GET", "POST"])
def create():
    if not session.get("admin"):
        return redirect(url_for("login"))

    if request.method == "POST":
        # თუ აღწერა ცარიელია, ავტომატურად ჩაიწერება ცარიელი ტექსტი
        description = request.form.get("description", "").strip()
        
        conn = get_db()
        conn.execute("""
            INSERT INTO Food(Name, Image, Description, Price)
            VALUES(?, ?, ?, ?)
        """, (
            request.form["name"],
            request.form["image"],
            description,
            request.form["price"]
        ))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    return render_template("create_product.html")



@app.route("/product/delete/<int:id>")
def delete(id):
    if not session.get("admin"):
        return redirect(url_for("login"))

    conn = get_db()
    conn.execute("DELETE FROM Food WHERE Id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    conn = get_db()
    cart = session.get("cart", {})
    items = []
    total = 0

    for fid, qty in cart.items():
        food = conn.execute("SELECT * FROM Food WHERE Id=?", (fid,)).fetchone()
        if food:
            subtotal = food["Price"] * qty
            total += subtotal
            items.append({"name": food["Name"], "qty": qty, "subtotal": subtotal})

    if request.method == "POST":
        table = request.form["table_number"]
        conn.execute("INSERT INTO Orders(Name, Total) VALUES(?, ?)", (f"Table {table}", total))
        conn.commit()
        conn.close()
        session["cart"] = {}
        flash("Order placed!")
        return redirect(url_for("index"))

    conn.close()
    return render_template("checkout.html", items=items, total=total)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
