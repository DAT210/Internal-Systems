from flask import render_template
import mysql.connector

get_queries = {
    # Get all courses
    "get_courses": "SELECT c_id, c_name, price FROM course",

    # Get course ingredients by c_id
    "get_ingredients_by_course": "SELECT i.i_id, i_name, available FROM ingredient AS i INNER JOIN course_ingredient AS ci ON i.i_id=ci.i_id WHERE c_id={c_id}",

    # Get all ingredients
    "get_ingredients": "SELECT i_id, i_name, available FROM ingredient",

    # Get allergenes by ingredient
    "get_allergenes_by_ingredient": "SELECT a.a_id, a.a_name FROM allergene AS a INNER JOIN ingredient_allergene AS ia ON a.a_id=ia.a_id WHERE ia.i_id={i_id}",

    # Get all allergenes
    "get_allergenes": "SELECT a_id, a_name FROM allergene"
}

def get_courses(db):
    cur = db.cursor()
    courses = []

    try:
        cur.execute(get_queries["get_courses"])
        for (c_id, c_name, price) in cur:
            courses.append({
                "c_id": str(c_id),
                "c_name": str(c_name),
                "price": str(price),
                "ingredients": []
            })
    except mysql.connector.Error as err:
        return render_template("error.html", msg=err)
    finally:
        cur.close()

    for c in courses:
        c["ingredients"] = get_ingredients_by_course(db, c["c_id"])
    return courses


def get_ingredients(db):
    cur = db.cursor()
    ingredients = []

    try:
        cur.execute(get_queries["get_ingredients"])
        for (i_id, i_name, available) in cur:
            ingredients.append({
                "i_id": str(i_id),
                "i_name": str(i_name),
                "available": str(available),
                "allergenes": []
            })
    except mysql.connector.Error as err:
        return render_template("error.html", msg=err)
    finally:
        cur.close()

    for i in ingredients:
        i["allergenes"] = get_allergenes_by_ingredient(db, i["i_id"])
    return ingredients


def get_allergenes(db):
    cur = db.cursor()
    allergenes = []

    try:
        cur.execute(get_queries["get_allergenes"])
        for (a_id, a_name) in cur:
            allergenes.append({
                "a_id": str(a_id),
                "a_name": str(a_name)
            })
        return allergenes
    except mysql.connector.Error as err:
        return render_template("error.html", msg=err)
    finally:
        cur.close()


def get_ingredients_by_course(db, c_id):
    cur = db.cursor()
    ingredients = []

    try:
        cur.execute(get_queries["get_ingredients_by_course"].replace("{c_id}", c_id))
        for (i_id, i_name, available) in cur:
            ingredients.append({
                "i_id": str(i_id),
                "i_name": str(i_name),
                "available": str(available),
                "allergenes": []
            })
    except mysql.connector.Error as err:
        return render_template("error.html", msg=err)
    finally:
        cur.close()

    for i in ingredients:
        i["allergenes"] = get_allergenes_by_ingredient(db, i["i_id"])
    return ingredients


def get_allergenes_by_ingredient(db, i_id):
    cur = db.cursor()
    allergenes = []

    try:
        cur.execute(get_queries["get_allergenes_by_ingredient"].replace("{i_id}", i_id))
        for (a_id, a_name) in cur:
            allergenes.append({
                "a_id": str(a_id),
                "a_name": str(a_name)
            })
        return allergenes
    except mysql.connector.Error as err:
        return render_template("error.html", msg=err)
    finally:
        cur.close()