from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB වෙත සම්බන්ධ වීම
client = MongoClient("mongodb://localhost:27017/")
db = client["smartmove_db"]
passengers_collection = db["passengers"]


@app.route("/")
def home():
    return "<h1>Welcome to SmartMove Home Page!</h1><br><a href='/register'>Go to Register Page</a>"


# GET සහ POST ක්‍රම දෙකම මෙතනට ඇතුළත් කර ඇත
@app.route("/register", methods=["GET", "POST"])
def register():
    # රෙජිස්ටර් වූ බව පෙන්වීමට විචල්‍යයක් (variable)
    success_message = False

    if request.method == "POST":
        # HTML ෆෝම් එකෙන් එවන දත්ත ලබා ගැනීම
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("psw")

        # දත්ත එකතුවක් (Dictionary) ලෙස සකස් කිරීම
        passenger_data = {
            "name": name,
            "email": email,
            "password": password
        }

        # සකස් කළ දත්ත MongoDB collection එකට ඇතුළත් කිරීම
        passengers_collection.insert_one(passenger_data)
        success_message = True

    # MongoDB එකේ තියෙන සියලුම මගීන්ගේ දත්ත ලබාගැනීම
    passengers_list = list(passengers_collection.find())

    # දත්ත සහ ෆෝම් එක සහිත පිටුව පෙන්වීම
    return render_template("index.html", passengers=passengers_list, success=success_message)


@app.route("/login")
def login():
    return "<h1>Login Page - ඉදිරියේදී නිර්මාණය කෙරේ!</h1>"


if __name__ == "__main__":
    app.run(debug=True)