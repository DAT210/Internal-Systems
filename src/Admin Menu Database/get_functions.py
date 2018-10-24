from flask import render_template
from exceptions import *
import types
import mysql.connector
from mysql.connector import IntegrityError, DataError, Error

get_queries = {
    # Get all courses
    "get_courses": "SELECT c_id, c_name, ca_id, info, price FROM course",

    # Get last course by id
    "get_course_end": "SELECT c_id, c_name, ca_id, info, price FROM course ORDER BY c_id DESC LIMIT 1",

    # Get course ingredients by c_id
    "get_ingredients_by_course": "SELECT i.i_id, i_name, available FROM ingredient AS i INNER JOIN course_ingredient AS ci ON i.i_id=ci.i_id WHERE c_id={c_id}",

    # Get all ingredients
    "get_ingredients": "SELECT i_id, i_name, available FROM ingredient",

    # Get last ingredient by id
    "get_ingredient_end": "SELECT i_id, i_name, available FROM ingredient ORDER BY i_id DESC LIMIT 1",

    # Get allergenes by ingredient
    "get_allergenes_by_ingredient": "SELECT a.a_id, a.a_name FROM allergene AS a INNER JOIN ingredient_allergene AS ia ON a.a_id=ia.a_id WHERE ia.i_id={i_id}",

    # Get all allergenes
    "get_allergenes": "SELECT a_id, a_name FROM allergene",

    # Get last allergene by id
    "get_allergene_end": "SELECT a_id, a_name FROM allergene ORDER BY a_id DESC LIMIT 1",

    # Get all categories
    "get_categories": "SELECT ca_id, ca_name FROM category",

    # Get last category by id
    "get_category_end": "SELECT ca_id, ca_name FROM category ORDER BY ca_id DESC LIMIT 1",

    # Get all selection categories
    "get_selection_categories": "SELECT sc_id, sc_name FROM selection_category",

    # Get last selection category by id
    "get_selection_category_end": "SELECT sc_id, sc_name FROM selection_category ORDER BY sc_id DESC LIMIT 1",

    # Get all selections
    "get_selections": "SELECT s_id, s_name, sc_id, i_id FROM selection",

    # Get last selection by id
    "get_selection_end": "SELECT s_id, s_name, sc_id, i_id FROM selection ORDER BY sc_id DESC LIMIT 1",

    # Get selections by course
    "get_selections_by_course": "SELECT s.s_id, s_name, s.sc_id, s.i_id FROM selection AS s INNER JOIN course_selection as cs ON s.s_id=cs.s_id WHERE cs.c_id={c_id}"
}

def get_courses(db):
    cur = db.cursor()
    courses = []

    try:
        cur.execute(get_queries["get_courses"])
        for (c_id, c_name, ca_id, info, price) in cur:
            courses.append({
                "c_id": str(c_id),
                "c_name": str(c_name),
                "ca_id": str(ca_id),
                "info": str(info),
                "price": str(price),
                "ingredients": [],
                "selections": []
            })
    finally:
        cur.close()

    for c in courses:
        c["ingredients"] = get_ingredients_by_course(db, c["c_id"])
    for c in courses:
        c["selections"] = get_selections_by_course(db, c["c_id"])
    return courses


def get_course_end(db):
    cur = db.cursor()
    courses = []

    try:
        cur.execute(get_queries["get_course_end"])
        for (c_id, c_name, ca_id, info, price) in cur:
            courses.append({
                "c_id": str(c_id),
                "c_name": str(c_name),
                "ca_id": str(ca_id),
                "info": str(info),
                "price": str(price),
                "ingredients": [],
                "selections": []
            })
    finally:
        cur.close()

    for c in courses:
        c["ingredients"] = get_ingredients_by_course(db, c["c_id"])
    for c in courses:
        c["selections"] = get_selections_by_course(db, c["c_id"])
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


def get_ingredient_end(db):
    cur = db.cursor()
    ingredients = []

    try:
        cur.execute(get_queries["get_ingredient_end"])
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
    finally:
        cur.close()


def get_allergene_end(db):
    cur = db.cursor()
    allergenes = []

    try:
        cur.execute(get_queries["get_allergene_end"])
        for (a_id, a_name) in cur:
            allergenes.append({
                "a_id": str(a_id),
                "a_name": str(a_name)
            })
        return allergenes
    finally:
        cur.close()


def get_categories(db):
    cur = db.cursor()
    categories = []

    try:
        cur.execute(get_queries["get_categories"])
        for (ca_id, ca_name) in cur:
            categories.append({
                "ca_id": str(ca_id),
                "ca_name": str(ca_name)
            })
        return categories
    finally:
        cur.close()


def get_category_end(db):
    cur = db.cursor()
    categories = []

    try:
        cur.execute(get_queries["get_category_end"])
        for (ca_id, ca_name) in cur:
            categories.append({
                "ca_id": str(ca_id),
                "ca_name": str(ca_name)
            })
        return categories
    finally:
        cur.close()


def get_categories_dictionary(db):
    cur = db.cursor()
    categories = {}

    try:
        cur.execute(get_queries["get_categories"])
        for (ca_id, ca_name) in cur:
            categories[str(ca_id)] = {
                "ca_id": str(ca_id),
                "ca_name": str(ca_name)
            }
        return categories
    finally:
        cur.close()


def get_selection_categories(db):
    cur = db.cursor()
    selection_categories = []

    try:
        cur.execute(get_queries["get_selection_categories"])
        for (sc_id, sc_name) in cur:
            selection_categories.append({
                "sc_id": str(sc_id),
                "sc_name": str(sc_name)
            })
        return selection_categories
    finally:
        cur.close()


def get_selection_category_end(db):
    cur = db.cursor()
    selection_categories = []

    try:
        cur.execute(get_queries["get_selection_category_end"])
        for (sc_id, sc_name) in cur:
            selection_categories.append({
                "sc_id": str(sc_id),
                "sc_name": str(sc_name)
            })
        return selection_categories
    finally:
        cur.close()


def get_selections(db):
    cur = db.cursor()
    selections = []

    try:
        cur.execute(get_queries["get_selections"])
        for (s_id, s_name, sc_id, i_id) in cur:
            selections.append({
                "s_id": str(s_id),
                "s_name": str(s_name),
                "sc_id": str(sc_id),
                "i_id": str(i_id)
            })
        return selections
    finally:
        cur.close()


def get_selection_end(db):
    cur = db.cursor()
    selections = []

    try:
        cur.execute(get_queries["get_selection_end"])
        for (s_id, s_name, sc_id, i_id) in cur:
            selections.append({
                "s_id": str(s_id),
                "s_name": str(s_name),
                "sc_id": str(sc_id),
                "i_id": str(i_id)
            })
        return selections
    finally:
        cur.close()


def get_ingredients_by_course(db, c_id):
    cur = db.cursor()
    ingredients = []

    try:
        if c_id == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(get_queries["get_ingredients_by_course"].replace("{c_id}", str(c_id)))
        for (i_id, i_name, available) in cur:
            ingredients.append({
                "i_id": str(i_id),
                "i_name": str(i_name),
                "available": str(available),
                "allergenes": []
            })
    except (Error) as err:
        if 'Unknown column' in str(err):
            return INVALID_TYPE_EXCEPTION
        raise err
    finally:
        cur.close()
    for i in ingredients:
        i["allergenes"] = get_allergenes_by_ingredient(db, i["i_id"])
    return ingredients


def get_allergenes_by_ingredient(db, i_id):
    cur = db.cursor()
    allergenes = []

    try:
        if i_id == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(get_queries["get_allergenes_by_ingredient"].replace("{i_id}", str(i_id)))
        for (a_id, a_name) in cur:
            allergenes.append({
                "a_id": str(a_id),
                "a_name": str(a_name)
            })
        return allergenes
    except (Error) as err:
        if 'Unknown column' in str(err):
            return INVALID_TYPE_EXCEPTION
        raise err
    finally:
        cur.close()


def get_selections_by_course(db, c_id):
    cur = db.cursor()
    selections = []

    try:
        if c_id == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(get_queries["get_selections_by_course"].replace("{c_id}", str(c_id)))
        for (s_id, s_name, sc_id, i_id) in cur:
            selections.append({
                "s_id": str(s_id),
                "s_name": str(s_name),
                "sc_id": str(sc_id),
                "i_id": str(i_id)
            })
        return selections
    except (Error) as err:
        if 'Unknown column' in str(err):
            return INVALID_TYPE_EXCEPTION
        raise err
    finally:
        cur.close()