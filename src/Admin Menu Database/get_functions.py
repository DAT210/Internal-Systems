from flask import render_template
from exceptions import *
import types
import mysql.connector
from mysql.connector import IntegrityError, DataError, Error

get_queries = {
    # Get all courses
    "get_courses": "SELECT c_id, c_name, ca_id, info, price FROM course ORDER BY c_id ASC",

    # Get course by c_id
    "get_course_by_id": "SELECT c_id, c_name, ca_id, info, price FROM course WHERE c_id={c_id}",

    # Get last course by id
    "get_course_end": "SELECT c_id, c_name, ca_id, info, price FROM course ORDER BY c_id DESC LIMIT 1",

    # Get course ingredients by c_id
    "get_ingredients_by_course": "SELECT i.i_id, i_name, available FROM ingredient AS i INNER JOIN course_ingredient AS ci ON i.i_id=ci.i_id WHERE c_id={c_id}",

    # Get all ingredients
    "get_ingredients": "SELECT i_id, i_name, available FROM ingredient ORDER BY i_id ASC",

    # Get ingredient by i_id
    "get_ingredient_by_id": "SELECT i_id, i_name, available FROM ingredient WHERE i_id={i_id}",

    # Get last ingredient by id
    "get_ingredient_end": "SELECT i_id, i_name, available FROM ingredient ORDER BY i_id DESC LIMIT 1",

    # Get allergenes by ingredient
    "get_allergenes_by_ingredient": "SELECT a.a_id, a.a_name FROM allergene AS a INNER JOIN ingredient_allergene AS ia ON a.a_id=ia.a_id WHERE ia.i_id={i_id}",

    # Get all allergenes
    "get_allergenes": "SELECT a_id, a_name FROM allergene ORDER BY a_id ASC",

    # Get allergene by a_id
    "get_allergene_by_id": "SELECT a_id, a_name FROM allergene WHERE a_id={a_id}",

    # Get last allergene by id
    "get_allergene_end": "SELECT a_id, a_name FROM allergene ORDER BY a_id DESC LIMIT 1",

    # Get all categories
    "get_categories": "SELECT ca_id, ca_name FROM category ORDER BY ca_id ASC",

    # Get category by ca_id
    "get_category_by_id": "SELECT ca_id, ca_name FROM category WHERE ca_id={ca_id}",

    # Get last category by id
    "get_category_end": "SELECT ca_id, ca_name FROM category ORDER BY ca_id DESC LIMIT 1",

    # Get all selection categories
    "get_selection_categories": "SELECT sc_id, sc_name FROM selection_category ORDER BY sc_id ASC",

    # Get selection_category by sc_id
    "get_selection_category_by_id": "SELECT sc_id, sc_name FROM selection_category WHERE sc_id={sc_id}",

    # Get last selection category by id
    "get_selection_category_end": "SELECT sc_id, sc_name FROM selection_category ORDER BY sc_id DESC LIMIT 1",

    # Get all selections sorted by s_id ascending
    "get_selections": "SELECT s_id, s_name, sc_id, i_id, s_price FROM selection ORDER BY s_id ASC",

    # Get selections by s_id
    "get_selection_by_id": "SELECT s_id, s_name, sc_id, i_id, s_price FROM selection WHERE s_id={s_id}",

    # Get last selection by id
    "get_selection_end": "SELECT s_id, s_name, sc_id, i_id, s_price FROM selection ORDER BY sc_id DESC LIMIT 1",

    # Get selections by course
    "get_selections_by_course": "SELECT s.s_id, s_name, s.sc_id, s.i_id, s.s_price FROM selection AS s INNER JOIN course_selection as cs ON s.s_id=cs.s_id WHERE cs.c_id={c_id}"
}

def __get_courses__(db, query):
    cur = db.cursor()
    courses = []

    try:
        cur.execute(query)
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
    except (DataError):
        return INPUT_TOO_LONG_EXCEPTION
    finally:
        cur.close()

    for c in courses:
        c["ingredients"] = get_ingredients_by_course(db, c["c_id"])
    for c in courses:
        c["selections"] = get_selections_by_course(db, c["c_id"])
    return courses


def __get_courses_dictionary__(db, query):
    cur = db.cursor()
    courses = {}

    try:
        cur.execute(query)
        for (c_id, c_name, ca_id, info, price) in cur:
            courses[str(c_id)] = {
                "c_id": str(c_id),
                "c_name": str(c_name),
                "ca_id": str(ca_id),
                "info": str(info),
                "price": str(price),
                "ingredients": [],
                "selections": []
            }
    except (DataError):
        return INPUT_TOO_LONG_EXCEPTION
    finally:
        cur.close()

    for c in courses:
        c["ingredients"] = get_ingredients_by_course(db, c["c_id"])
    for c in courses:
        c["selections"] = get_selections_by_course(db, c["c_id"])
    return courses


def get_courses(db, as_dict = False):
    if as_dict:
        return __get_courses_dictionary__(db, get_queries["get_courses"])
    else:
        return __get_courses__(db, get_queries["get_courses"])


def get_course_end(db, as_dict = False):
    if as_dict:
        return __get_courses_dictionary__(db, get_queries["get_course_end"])
    else:
        return __get_courses__(db, get_queries["get_course_end"])


def get_course_by_id(db, c_id, as_dict = False):
    if c_id == None:
        return EMPTY_INPUT_EXCEPTION
    if as_dict:
        return __get_courses_dictionary__(db, get_queries["get_course_by_id"].replace("{c_id}", str(c_id)))
    else:
        return __get_courses__(db, get_queries["get_course_by_id"].replace("{c_id}", str(c_id)))


def __get_ingredients__(db, query):
    cur = db.cursor()
    ingredients = []

    try:
        cur.execute(query)
        for (i_id, i_name, available) in cur:
            ingredients.append({
                "i_id": str(i_id),
                "i_name": str(i_name),
                "available": str(available),
                "allergenes": []
            })
    except (DataError):
        return INPUT_TOO_LONG_EXCEPTION
    finally:
        cur.close()

    for i in ingredients:
        i["allergenes"] = get_allergenes_by_ingredient(db, i["i_id"])
    return ingredients


def __get_ingredients_dictionary__(db, query):
    cur = db.cursor()
    ingredients = {}

    try:
        cur.execute(query)
        for (i_id, i_name, available) in cur:
            ingredients[str(i_id)] = {
                "i_id": str(i_id),
                "i_name": str(i_name),
                "available": str(available),
                "allergenes": []
            }
    except (DataError):
        return INPUT_TOO_LONG_EXCEPTION
    finally:
        cur.close()

    for _, i in ingredients.items():
        i["allergenes"] = get_allergenes_by_ingredient(db, i["i_id"])
    return ingredients


def get_ingredients(db, as_dict = False):
    if as_dict:
        return __get_ingredients_dictionary__(db, get_queries["get_ingredients"])
    else:
        return __get_ingredients__(db, get_queries["get_ingredients"])


def get_ingredient_end(db, as_dict = False):
    if as_dict:
        return __get_ingredients_dictionary__(db, get_queries["get_ingredient_end"])
    else:
        return __get_ingredients__(db, get_queries["get_ingredient_end"])


def get_ingredient_by_id(db, i_id, as_dict = False):
    if i_id == None:
        return EMPTY_INPUT_EXCEPTION
    if as_dict:
        return __get_ingredients_dictionary__(db, get_queries["get_ingredient_by_id"].replace("{i_id}", str(i_id)))
    else:
        return __get_ingredients__(db, get_queries["get_ingredient_by_id"].replace("{i_id}", str(i_id)))


def __get_allergenes__(db, query):
    cur = db.cursor()
    allergenes = []

    try:
        cur.execute(query)
        for (a_id, a_name) in cur:
            allergenes.append({
                "a_id": str(a_id),
                "a_name": str(a_name)
            })
    except (DataError):
        return INPUT_TOO_LONG_EXCEPTION
    finally:
        cur.close()

    return allergenes


def __get_allergenes_dictionary__(db, query):
    cur = db.cursor()
    allergenes = {}

    try:
        cur.execute(query)
        for (a_id, a_name) in cur:
            allergenes[str(a_id)] = {
                "a_id": str(a_id),
                "a_name": str(a_name)
            }
    except (DataError):
        return INPUT_TOO_LONG_EXCEPTION
    finally:
        cur.close()

    return allergenes


def get_allergenes(db, as_dict = False):
    if as_dict:
        return __get_allergenes_dictionary__(db, get_queries["get_allergenes"])
    else:
        return __get_allergenes__(db, get_queries["get_allergenes"])


def get_allergene_end(db, as_dict = False):
    if as_dict:
        return __get_allergenes_dictionary__(db, get_queries["get_allergene_end"])
    else:
        return __get_allergenes__(db, get_queries["get_allergene_end"])


def get_allergene_by_id(db, a_id, as_dict = False):
    if a_id == None:
        return EMPTY_INPUT_EXCEPTION
    if as_dict:
        return __get_allergenes_dictionary__(db, get_queries["get_allergene_by_id"].replace("{a_id}", str(a_id)))
    else:
        return __get_allergenes__(db, get_queries["get_allergene_by_id"].replace("{a_id}", str(a_id)))

def __get_categories__(db, query):
    cur = db.cursor()
    categories = []

    try:
        cur.execute(query)
        for (ca_id, ca_name) in cur:
            categories.append({
                "ca_id": str(ca_id),
                "ca_name": str(ca_name)
            })
        return categories
    finally:
        cur.close()


def __get_categories_dictionary__(db, query):
    cur = db.cursor()
    categories = {}

    try:
        cur.execute(query)
        for (ca_id, ca_name) in cur:
            categories[str(ca_id)] = {
                "ca_id": str(ca_id),
                "ca_name": str(ca_name)
            }
        return categories
    finally:
        cur.close()


def get_categories(db, as_dict = False):
    if as_dict:
        return __get_categories_dictionary__(db, get_queries["get_categories"])
    else:
        return __get_categories__(db, get_queries["get_categories"])


def get_category_end(db, as_dict = False):
    if as_dict:
        return __get_categories_dictionary__(db, get_queries["get_category_end"])
    else:
        return __get_categories__(db, get_queries["get_category_end"])


def get_category_by_id(db, ca_id, as_dict = False):
    if ca_id == None:
        return EMPTY_INPUT_EXCEPTION
    if as_dict:
        return __get_categories_dictionary__(db, get_queries["get_category_by_id"].replace("{ca_id}", str(ca_id)))
    else:
        return __get_categories__(db, get_queries["get_category_by_id"].replace("{ca_id}", str(ca_id)))


def __get_selection_categories__(db, query):
    cur = db.cursor()
    selection_categories = []

    try:
        cur.execute(query)
        for (sc_id, sc_name) in cur:
            selection_categories.append({
                "sc_id": str(sc_id),
                "sc_name": str(sc_name)
            })
        return selection_categories
    finally:
        cur.close()


def __get_selection_categories_dictionary__(db, query):
    cur = db.cursor()
    selection_categories = {}

    try:
        cur.execute(query)
        for (sc_id, sc_name) in cur:
            selection_categories[str(sc_id)] = {
                "sc_id": str(sc_id),
                "sc_name": str(sc_name)
            }
        return selection_categories
    finally:
        cur.close()


def get_selection_categories(db, as_dict = False):
    if as_dict:
        return __get_selection_categories_dictionary__(db, get_queries["get_selection_categories"])
    else:
        return __get_selection_categories__(db, get_queries["get_selection_categories"])


def get_selection_category_end(db, as_dict = False):
    if as_dict:
        return __get_selection_categories_dictionary__(db, get_queries["get_selection_category_end"])
    else:
        return __get_selection_categories__(db, get_queries["get_selection_category_end"])


def get_selection_category_by_id(db, sc_id, as_dict = False):
    if sc_id == None:
        return EMPTY_INPUT_EXCEPTION
    if as_dict:
        return __get_selection_categories_dictionary__(db, get_queries["get_selection_category_by_id"].replace("{sc_id}", str(sc_id)))
    else:
        return __get_selection_categories__(db, get_queries["get_selection_category_by_id"].replace("{sc_id}", str(sc_id)))


def __get_selections__(db, query):
    cur = db.cursor()
    selections = []

    try:
        cur.execute(query)
        for (s_id, s_name, sc_id, i_id, s_price) in cur:
            selections.append({
                "s_id": str(s_id),
                "s_name": str(s_name),
                "sc_id": str(sc_id),
                "i_id": str(i_id),
                "s_price": str(s_price)
            })
        return selections
    finally:
        cur.close()


def __get_selections_dictionary__(db, query):
    cur = db.cursor()
    selections = {}

    try:
        cur.execute(query)
        for (s_id, s_name, sc_id, i_id, s_price) in cur:
            selections[str(s_id)] = {
                "s_id": str(s_id),
                "s_name": str(s_name),
                "sc_id": str(sc_id),
                "i_id": str(i_id),
                "s_price": str(s_price)
            }
        return selections
    finally:
        cur.close()


def get_selections(db, as_dict = False):
    if as_dict:
        return __get_selections_dictionary__(db, get_queries["get_selections"])
    else:
        return __get_selections__(db, get_queries["get_selections"])


def get_selection_end(db, as_dict = False):
    if as_dict:
        return __get_selections_dictionary__(db, get_queries["get_selection_end"])
    else:
        return __get_selections__(db, get_queries["get_selection_end"])


def get_selection_by_id(db, s_id, as_dict = False):
    if s_id == None:
        return EMPTY_INPUT_EXCEPTION
    if as_dict:
        return __get_selections_dictionary__(db, get_queries["get_selection_by_id"].replace("{s_id}", str(s_id)))
    else:
        return __get_selections__(db, get_queries["get_selection_by_id"].replace("{s_id}", str(s_id)))


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
        for (s_id, s_name, sc_id, i_id, s_price) in cur:
            selections.append({
                "s_id": str(s_id),
                "s_name": str(s_name),
                "sc_id": str(sc_id),
                "i_id": str(i_id),
                "s_price": str(s_price)
            })
        return selections
    except (Error) as err:
        if 'Unknown column' in str(err):
            return INVALID_TYPE_EXCEPTION
        raise err
    finally:
        cur.close()