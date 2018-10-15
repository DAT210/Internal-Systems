from flask import Flask, render_template, request, g, redirect, url_for
import json
import mysql.connector
from get_functions import *
from remove_functions import *
from insert_functions import *
from update_functions import *

app = Flask(__name__)

app.debug = True

isAdmin = True

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
    return render_template("index.html", courses=courses, ingredients=ingredients, allergenes=allergenes, admin=isAdmin)


## DATABASE GET REQUEST REMOVE FUNCTIONS ##
@app.route("/remove_course", methods=["GET"])
def remove_course_db():
    c_id = request.args.get("c_id", None)
    if c_id != None:
        remove_course(get_db(), c_id)
    return render_template("course_display.html", courses=get_courses(get_db()), admin=isAdmin)


@app.route("/remove_ingredient_from_course", methods=["GET"])
def remove_ingredient_from_course_db():
    c_id = request.args.get("c_id", None)
    i_id = request.args.get("i_id", None)
    if c_id != None and i_id != None:
        remove_course_ingredient(get_db(), c_id, i_id)
    return render_template("course_display.html", courses=get_courses(get_db()), admin=isAdmin)


## DATABASE GET REQUEST GET FUNCTIONS ##
@app.route("/get_ingredients", methods=["GET"])
def get_ingredients_db():
    ingredients = get_ingredients(get_db())
    return json.dumps(ingredients)


@app.route("/get_allergenes", methods=["GET"])
def get_allergenes_db():
    allergenes = get_allergenes(get_db())
    return json.dumps(allergenes)


## DATABASE GET REQUEST INSERT FUNCTIONS ##
@app.route("/add_course", methods=["GET"])
def insert_course_db():
    # FIX CATEGORY, ADD FUNCTIONALITY FOR THIS SOON
    exception = insert_course(get_db(), "", 1, 0.0)
    if exception.message:
        print("\tEXCEPTION " + str(exception.code) + ": " + exception.message)
    return render_template("course_display.html", courses=get_courses(get_db()), admin=isAdmin)


@app.route("/add_ingredient_to_course", methods=["GET"])
def insert_course_ingredient_db():
    c_id = request.args.get("c_id", None)
    i_id = request.args.get("i_id", None)
    if c_id != None and i_id != None:
        insert_course_ingredient(get_db(), c_id, i_id)
    return render_template("course_display.html", courses=get_courses(get_db()), admin=isAdmin)


## DATABASE GET REQUEST UPDATE FUNCTIONS ##
@app.route("/edit_course_name", methods=["GET"])
def update_course_name_db():
    c_id = request.args.get("c_id", None)
    c_name = request.args.get("c_name", None)
    if c_id != None and c_name != None:
        update_course_name(get_db(), c_name, c_id)
    return render_template("course_display.html", courses=get_courses(get_db()), admin=isAdmin)


@app.route("/edit_course_price", methods=["GET"])
def update_course_price_db():
    c_id = request.args.get("c_id", None)
    price = request.args.get("price", None)
    if c_id != None and price != None:
        update_course_price(get_db(), price, c_id)
    return render_template("course_display.html", courses=get_courses(get_db()), admin=isAdmin)


if __name__ == "__main__":
    app.run()