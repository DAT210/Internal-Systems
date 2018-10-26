from flask import Flask, render_template, request, g, redirect, url_for
import json
import string
import mysql.connector
from get_functions import *
from remove_functions import *
from insert_functions import *
from update_functions import *

# Sindre Hvidsten

##################
# MISC FUNCTIONS #
##################

CHARS = list(string.ascii_lowercase)


def convert_number_to_unique_char_sequence(number):
    number -= 1
    char_sequence = []
    while number > 0:
        char_sequence.append(CHARS[number % 26])
        number //= 26
    char_sequence.reverse()
    return ''.join(char_sequence)
    

app = Flask(__name__)

app.debug = True

isAdmin = True

# CHANGE THIS INFORMATION FOR YOUR DATABASE ACCESS OK
user_info = {
    "username": "root",
    "password": "dat220pass",
    "database": "dat210_menu",
    "hostname": "localhost",
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
    allergenes = get_allergenes(get_db())
    categories = get_categories_dictionary(get_db())
    selections = get_selections(get_db())
    selection_categories = get_selection_categories_dictionary(get_db())
    return render_template("index.html", courses=courses, ingredients=ingredients, allergenes=allergenes, categories=categories, selections=selections, selection_categories=selection_categories, admin=isAdmin)


## GET THE DISPLAYS ##
@app.route("/get_course_display", methods=["GET"])
def get_course_display():
    return render_template("course_display.html", courses=get_courses(get_db()), categories=get_categories_dictionary(get_db()), admin=isAdmin)


@app.route("/get_ingredient_display", methods=["GET"])
def get_ingredient_display():
    return render_template("ingredient_display.html", ingredients=get_ingredients(get_db()), admin=isAdmin)


@app.route("/get_allergene_display", methods=["GET"])
def get_allergene_display():
    return render_template("allergene_display.html", allergenes=get_allergenes(get_db()), admin=isAdmin)


@app.route("/get_category_display", methods=["GET"])
def get_category_display():
    return render_template("category_display.html", categories=get_categories_dictionary(get_db()), admin=isAdmin)


@app.route("/get_selection_display", methods=["GET"])
def get_selection_display():
    return render_template("selection_display.html", selections=get_selections(get_db()), selection_categories=get_selection_categories_dictionary(get_db()), admin=isAdmin)


@app.route("/get_selection_category_display", methods=["GET"])
def get_selection_category_display():
    return render_template("selection_category_display.html", selection_categories=get_selection_categories_dictionary(get_db()), admin=isAdmin)


## DATABASE GET REQUEST REMOVE FUNCTIONS ##

## COURSES ##
@app.route("/remove_course", methods=["GET"])
def remove_course_db():
    c_id = request.args.get("c_id", None)
    if c_id != None:
        remove_course(get_db(), c_id)
    return ""


@app.route("/remove_ingredient_from_course", methods=["GET"])
def remove_ingredient_from_course_db():
    c_id = request.args.get("c_id", None)
    i_id = request.args.get("i_id", None)
    if c_id != None and i_id != None:
        remove_course_ingredient(get_db(), c_id, i_id)
    return ""


@app.route("/remove_selection_from_course", methods=["GET"])
def remove_selection_from_course_db():
    c_id = request.args.get("c_id", None)
    s_id = request.args.get("s_id", None)
    if c_id != None and s_id != None:
        remove_course_selection(get_db(), c_id, s_id)
    return ""


## INGREDIENTS ##
@app.route("/remove_ingredient", methods=["GET"])
def remove_ingredient_db():
    i_id = request.args.get("i_id", None)
    if i_id != None:
        remove_ingredient(get_db(), i_id)
    return ""


@app.route("/remove_allergene_from_ingredient", methods=["GET"])
def remove_ingredient_allergene_db():
    i_id = request.args.get("i_id", None)
    a_id = request.args.get("a_id", None)
    if i_id != None and a_id != None:
        remove_ingredient_allergene(get_db(), i_id, a_id)
    return ""


## ALLERGENES
@app.route("/remove_allergene", methods=["GET"])
def remove_allergene_db():
    a_id = request.args.get("a_id", None)
    if a_id != None:
        remove_allergene(get_db(), a_id)
    return ""


## DATABASE GET REQUEST GET FUNCTIONS ##
@app.route("/get_ingredients", methods=["GET"])
def get_ingredients_db():
    ingredients = get_ingredients(get_db())
    return json.dumps(ingredients)


@app.route("/get_allergenes", methods=["GET"])
def get_allergenes_db():
    allergenes = get_allergenes(get_db())
    return json.dumps(allergenes)


@app.route("/get_categories", methods=["GET"])
def get_categories_db():
    categories = get_categories(get_db())
    return json.dumps(categories)


@app.route("/get_selections", methods=["GET"])
def get_selections_db():
    selections = get_selections(get_db())
    return json.dumps(selections)


@app.route("/get_selection_categories", methods=["GET"])
def get_selection_categories_db():
    selection_categories = get_selection_categories(get_db())
    return json.dumps(selection_categories)


## DATABASE GET REQUEST INSERT FUNCTIONS ##

## COURSES ##
@app.route("/add_course", methods=["GET"])
def insert_course_db():
    insert_course(get_db(), "", 1, "No description available.", 1.0)

    new_course_id = get_course_end(get_db())[0]["c_id"]
    unique_string = convert_number_to_unique_char_sequence(int(new_course_id))
    update_course_name(get_db(), "course " + unique_string, new_course_id)

    return ""


@app.route("/add_ingredient_to_course", methods=["GET"])
def insert_course_ingredient_db():
    c_id = request.args.get("c_id", None)
    i_id = request.args.get("i_id", None)
    if c_id != None and i_id != None:
        insert_course_ingredient(get_db(), c_id, i_id)
    return ""


@app.route("/add_selection_to_course", methods=["GET"])
def insert_course_selection_db():
    c_id = request.args.get("c_id", None)
    s_id = request.args.get("s_id", None)
    if c_id != None and s_id != None:
        insert_course_selection(get_db(), c_id, s_id)
    return ""


## INGREDIENT ##
@app.route("/add_ingredient", methods=["GET"])
def insert_ingredient_db():
    insert_ingredient(get_db(), "", 1)

    new_ingredient_id = get_ingredient_end(get_db())[0]["i_id"]
    unique_string = convert_number_to_unique_char_sequence(int(new_ingredient_id))
    update_ingredient_name(get_db(), "ingredient " + unique_string, new_ingredient_id)

    return ""


@app.route("/add_allergene_to_ingredient", methods=["GET"])
def insert_ingredient_allergene_db():
    i_id = request.args.get("i_id", None)
    a_id = request.args.get("a_id", None)
    if i_id != None and a_id != None:
        insert_ingredient_allergene(get_db(), i_id, a_id)
    return ""


## ALLERGENE ##
@app.route("/add_allergene", methods=["GET"])
def insert_allergene_db():
    insert_allergene(get_db(), "")

    # WEIRD BUG:
    # For some reason allergene is sorted by name instead of id, need to find a fix for this, somehow

    new_allergene_id = get_allergene_end(get_db())[0]["a_id"]
    unique_string = convert_number_to_unique_char_sequence(int(new_allergene_id))
    update_allergene_name(get_db(), "allergene " + unique_string, new_allergene_id)

    return ""


## CATEGORY ##
@app.route("/add_category", methods=["GET"])
def insert_category_db():
    insert_category(get_db(), "")

    new_category_id = get_category_end(get_db())[0]["c_id"]
    unique_string = convert_number_to_unique_char_sequence(int(new_category_id))
    update_category_name(get_db(), "category " + unique_string, new_category_id)

    return ""


## SELECTION ##
@app.route("/add_selection", methods=["GET"])
def insert_selection_db():
    insert_selection(get_db(), "", 1, "NULL")

    new_selection_id = get_selection_end(get_db())[0]["s_id"]
    unique_string = convert_number_to_unique_char_sequence(int(new_selection_id))
    update_selection_name(get_db(), "selection " + unique_string, new_selection_id)

    return ""


## SELECTION CATEGORY ##
@app.route("/add_selection_category", methods=["GET"])
def insert_selection_category_db():
    insert_selection_category(get_db(), "")

    new_selection_category_id = get_selection_category_end(get_db())[0]["sc_id"]
    unique_string = convert_number_to_unique_char_sequence(int(new_selection_category_id))
    update_selection_category_name(get_db(), "selection category " + unique_string, new_selection_category_id)

    return ""


## DATABASE GET REQUEST UPDATE FUNCTIONS ##

## EDIT COURSES ##
@app.route("/edit_course_name", methods=["GET"])
def update_course_name_db():
    c_id = request.args.get("c_id", None)
    c_name = request.args.get("c_name", None)
    if c_id != None and c_name != None:
        update_course_name(get_db(), c_name, c_id)
    return ""


@app.route("/edit_course_price", methods=["GET"])
def update_course_price_db():
    c_id = request.args.get("c_id", None)
    price = request.args.get("price", None)
    if c_id != None and price != None:
        update_course_price(get_db(), price, c_id)
    return ""


@app.route("/edit_course_category", methods=["GET"])
def update_course_category_db():
    c_id = request.args.get("c_id", None)
    ca_id = request.args.get("ca_id", None)
    if c_id != None and ca_id != None:
        update_course_category(get_db(), ca_id, c_id)
    return ""


@app.route("/edit_course_description", methods=["GET"])
def update_course_description_db():
    c_id = request.args.get("c_id", None)
    description = request.args.get("description", None)
    if c_id != None and description != None:
        update_course_info(get_db(), description, c_id)
    return ""


## EDIT INGREDIENTS ##
@app.route("/edit_ingredient_name", methods=["GET"])
def update_ingredient_name_db():
    i_id = request.args.get("i_id", None)
    i_name = request.args.get("i_name", None)
    if i_id != None and i_name != None:
        update_ingredient_name(get_db(), i_name, i_id)
    return ""


## EDIT ALLERGENES ##
@app.route("/edit_allergene_name", methods=["GET"])
def update_allergene_name_db():
    a_id = request.args.get("a_id", None)
    a_name = request.args.get("a_name", None)
    if a_id != None and a_name != None:
        update_allergene_name(get_db(), a_name, a_id)
    return ""


if __name__ == "__main__":
    app.run()