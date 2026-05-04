from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "dev_secret_key"

client = MongoClient("mongodb://mongodb:27017/")
db = client["coffee_app"]


@app.route("/")
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/login")

    visits = list(db.visits.find())

    for visit in visits:
        visit["shop"] = db.shops.find_one({"_id": visit["shop_id"]})

    return render_template("dashboard.html", visits=visits)


@app.route("/add", methods=["GET", "POST"])
def add_shop():
    if "username" not in session:
        return redirect("/login")
        
    if request.method == "POST":
        name = request.form["name"]
        rating = int(request.form["rating"])
        notes = request.form.get("notes", "")


        shop = db.shops.find_one({"name": name})

        if not shop:
            shop_id = db.shops.insert_one({"name": name}).inserted_id
        else:
            shop_id = shop["_id"]

        db.visits.insert_one({
            "shop_id": shop_id,
            "rating": rating,
            "notes": notes
        })

        return redirect("/dashboard")

    return render_template("add_shop.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = db.users.find_one({"username": username})

        if existing_user:
            return "Username already exists."

        hashed_pw = generate_password_hash(password)

        db.users.insert_one({
            "username": username,
            "password": hashed_pw
        })

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = db.users.find_one({"username": username})

        if user and check_password_hash(user["password"], password):
            session["username"] = username
            return redirect("/dashboard")

        return "Invalid credentials."

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)