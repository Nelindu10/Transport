from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Connect
client = MongoClient("mongodb://localhost:27017/")
db = client["smartmove_db"]
passengers_collection = db["passengers"]


@app.route("/")
def home():
    return "<h1>Welcome to SmartMove Home Page!</h1><br><a href='/register'>Go to Register Page</a>"


# GET and POST include
@app.route("/register", methods=["GET", "POST"])
def register():
    # register una kiyanna variable
    success_message = False

    if request.method == "POST":
        # HTML form eke data ganima
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("psw")

        # data Dictionary lesa hadima
        passenger_data = {
            "name": name,
            "email": email,
            "password": password
        }

        # haduwa MongoDB collection eka insert kara
        passengers_collection.insert_one(passenger_data)
        success_message = True

    # MongoDB eken okkoma data gannawa
    passengers_list = list(passengers_collection.find())

    # data ha form eka thiyana ewa penwima
    return render_template("index.html", passengers=passengers_list, success=success_message)


@app.route("/login")
def login():
    return "<h1>Login Page - Next to update hode!</h1>"


if __name__ == "__main__":
    app.run(debug=True)