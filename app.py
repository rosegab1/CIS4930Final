from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://mongodb:27017/")
db = client["coffee_app"]


@app.route("/")
@app.route("/dashboard")
def dashboard():
    visits = list(db.visits.find())

    for visit in visits:
        visit["shop"] = db.shops.find_one({"_id": visit["shop_id"]})

    return render_template("dashboard.html", visits=visits)


@app.route("/add", methods=["GET", "POST"])
def add_shop():
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)