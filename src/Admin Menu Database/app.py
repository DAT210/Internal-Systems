from flask import Flask, render_template, request, g
import mysql.connector
from get_functions import *

app = Flask(__name__)

app.debug = True

# CHANGE THIS INFORMATION FOR YOUR DATABASE ACCESS OK
user_info = {
    "username": "root",
    "password": "dat220pass",
    "database": "dat210_menu",
    "hostname": "localhost"
}


app.config["DATABASE_USER"] = user_info["username"]
app.config["DATABASE_PASSWORD"] = user_info["password"]
app.config["DATABASE_DB"] = user_info["database"]
app.config["DATABASE_HOST"] = user_info["hostname"]
app.debug = True


def get_db():
    if not hasattr(g, "_database"):
        g._database = mysql.connector.connect(
            host=app.config["DATABASE_HOST"],
            user=app.config["DATABASE_USER"],
            password=app.config["DATABASE_PASSWORD"],
            database=app.config["DATABASE_DB"]
        )
    return g._database


@app.teardown_appcontext
def teardown_db(error):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    courses = get_courses(get_db())
    ingredients = get_ingredients(get_db())
    allergenes = get_allergenes(get_db()) # Maybe change name to triggers
    return render_template("index.html", courses=courses, ingredients=ingredients, allergenes=allergenes)


if __name__ == "__main__":
    app.run()