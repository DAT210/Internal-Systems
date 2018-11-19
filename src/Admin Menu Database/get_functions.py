from flask import render_template
from exceptions import *
import types
import mysql.connector
from mysql.connector import IntegrityError, DataError, Error

# Sindre Hvidsten #

# Please do not use the functions defined like __function__(),
# use the other defined functions instead.

get_queries = {
    # Get all courses
    "get_courses": "SELECT c_id, c_name, ca_id, info, price FROM course ORDER BY c_id ASC",

    # Get c_id and c_name from courses
    "get_courses_id_name": "SELECT c_id, c_name FROM course ORDER BY c_id ASC",

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
    "get_selections_by_course": "SELECT s.s_id, s.s_name, s.sc_id, s.i_id, s.s_price FROM selection AS s INNER JOIN course_selection AS cs ON s.s_id=cs.s_id WHERE cs.c_id={c_id}",

    # Get selections by ingredient
    "get_selections_by_ingredient": "SELECT s.s_id, s.s_name, s.sc_id, s.i_id, s.s_price FROM selection AS s WHERE s.i_id={i_id}"
}

def __get_courses__(db, query, as_dict):
    cur = db.cursor()
    courses = []
    if as_dict:
        courses = {}
        
    try:
        cur.execute(query)
        if as_dict:
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
        else:
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
    except Error as err:
        if 'Unknown column' in str(err):
            return INVALID_TYPE_EXCEPTION
        raise err

    finally:
        cur.close()

    if as_dict:
        for _, c in courses.items():
            c["ingredients"] = get_ingredients_by_course(db, c["c_id"])
        for _, c in courses.items():
            c["selections"] = get_selections_by_course(db, c["c_id"])
    else:
        for c in courses:
            c["ingredients"] = get_ingredients_by_course(db, c["c_id"])
        for c in courses:
            c["selections"] = get_selections_by_course(db, c["c_id"])
    return courses


def get_courses(db, as_dict = False):
    return __get_courses__(db, get_queries["get_courses"], as_dict)


def get_course_end(db, as_dict = False):
    return __get_courses__(db, get_queries["get_course_end"], as_dict)


def get_course_by_id(db, c_id, as_dict = False):
    if c_id == None:
        return EMPTY_INPUT_EXCEPTION
    return __get_courses__(db, get_queries["get_course_by_id"].replace("{c_id}", str(c_id)), as_dict)

def __get_courses_id_name__(db, query, as_dict):
    cur = db.cursor()
    courses = []
    if as_dict:
        courses = {}

    try:
        cur.execute(query)
        if as_dict:
            for (c_id, c_name) in cur:
                courses[str(c_id)] = {
                    "c_id": str(c_id),
                    "c_name": str(c_name),
                }
        else:
            for (c_id, c_name) in cur:
                courses.append({
                    "c_id": str(c_id),
                    "c_name": str(c_name),
                })
            return courses
    except (DataError):
        return UNKKNOWN_REFERENCE_EXCEPTION
    finally:
        cur.close()

    return courses


def get_courses_id_name(db, as_dict = False):
    return __get_courses_id_name__(db, get_queries["get_courses_id_name"], as_dict)


def __get_ingredients__(db, query, as_dict, with_allergenes, with_selections):
    cur = db.cursor()
    ingredients = []
    if as_dict:
        ingredients = {}
    try:
        cur.execute(query)
        if as_dict:
            for (i_id, i_name, available) in cur:
                ingredients[str(i_id)] = {
                    "i_id": str(i_id),
                    "i_name": str(i_name),
                    "available": str(available),
                    "allergenes": [],
                    "selections": []
                }
        else:
            for (i_id, i_name, available) in cur:
                ingredients.append({
                    "i_id": str(i_id),
                    "i_name": str(i_name),
                    "available": str(available),
                    "allergenes": [],
                    "selections": []
                })

    except (DataError):
        return INPUT_TOO_LONG_EXCEPTION
    except Error as err:
        if 'Unknown column' in str(err):
            return INVALID_TYPE_EXCEPTION
        raise err
    finally:
        cur.close()

    if as_dict:
        if with_allergenes:
            for _, i in ingredients.items():
                i["allergenes"] = get_allergenes_by_ingredient(db, i["i_id"])
        if with_selections:
            for _, i in ingredients.items():
                i["selections"] = get_selections_by_ingredient(db, i["i_id"])
    else:
        if with_allergenes:
            for i in ingredients:
                i["allergenes"] = get_allergenes_by_ingredient(db, i["i_id"])
        if with_selections:
            for i in ingredients:
                i["selections"] = get_selections_by_ingredient(db, i["i_id"])
    return ingredients


def get_ingredients(db, as_dict = False, with_allergenes = True, with_selections = True):
    return __get_ingredients__(db, get_queries["get_ingredients"], as_dict, with_allergenes, with_selections)


def get_ingredient_end(db, as_dict = False, with_allergenes = True, with_selections = True):
    return __get_ingredients__(db, get_queries["get_ingredient_end"], as_dict, with_allergenes, with_selections)


def get_ingredient_by_id(db, i_id, as_dict = False, with_allergenes = True, with_selections = True):
    if i_id == None:
        return EMPTY_INPUT_EXCEPTION
    return __get_ingredients__(db, get_queries["get_ingredient_by_id"].replace("{i_id}", str(i_id)), as_dict, with_allergenes, with_selections)


def get_ingredients_by_course(db, c_id, as_dict = False, with_allergenes = True, with_selections = True):
    if c_id == None:
        return EMPTY_INPUT_EXCEPTION
    return __get_ingredients__(db, get_queries["get_ingredients_by_course"].replace("{c_id}", str(c_id)), as_dict, with_allergenes, with_selections)


def __get_allergenes__(db, query, as_dict):
    cur = db.cursor()
    allergenes = []
    if as_dict:
        allergenes = {}
    try:
        cur.execute(query)
        if as_dict:
            for (a_id, a_name) in cur:
                allergenes[str(a_id)] = {
                    "a_id": str(a_id),
                    "a_name": str(a_name)
                }
        else:
            for (a_id, a_name) in cur:
                allergenes.append({
                    "a_id": str(a_id),
                    "a_name": str(a_name)
                })
    except (DataError):
        return INPUT_TOO_LONG_EXCEPTION
    except Error as err:
        if 'Unknown column' in str(err):
            return INVALID_TYPE_EXCEPTION
        raise err
    finally:
        cur.close()

    return allergenes
    

def get_allergenes(db, as_dict = False):
    return __get_allergenes__(db, get_queries["get_allergenes"], as_dict)


def get_allergene_end(db, as_dict = False):
    return __get_allergenes__(db, get_queries["get_allergene_end"], as_dict)


def get_allergene_by_id(db, a_id, as_dict = False):
    if a_id == None:
        return EMPTY_INPUT_EXCEPTION
    return __get_allergenes__(db, get_queries["get_allergene_by_id"].replace("{a_id}", str(a_id)), as_dict)


def get_allergenes_by_ingredient(db, i_id, as_dict = False):
    if i_id == None:
        return EMPTY_INPUT_EXCEPTION
    return __get_allergenes__(db, get_queries["get_allergenes_by_ingredient"].replace("{i_id}", str(i_id)), as_dict)


def __get_categories__(db, query, as_dict):
    cur = db.cursor()
    categories = []
    if as_dict:
        categories = {}

    try:
        cur.execute(query)
        if as_dict:
            for (ca_id, ca_name) in cur:
                categories[str(ca_id)] = {
                    "ca_id": str(ca_id),
                    "ca_name": str(ca_name)
                }
        else:
            for (ca_id, ca_name) in cur:
                categories.append({
                    "ca_id": str(ca_id),
                    "ca_name": str(ca_name)
                })
    except Error as err:
        if 'Unknown column' in str(err):
            return INVALID_TYPE_EXCEPTION
        raise err
    finally:
        cur.close()
    return categories


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
    return __get_categories__(db, get_queries["get_categories"], as_dict)


def get_category_end(db, as_dict = False):
    return __get_categories__(db, get_queries["get_category_end"], as_dict)


def get_category_by_id(db, ca_id, as_dict = False):
    if ca_id == None:
        return EMPTY_INPUT_EXCEPTION
    return __get_categories__(db, get_queries["get_category_by_id"].replace("{ca_id}", str(ca_id)), as_dict)


def __get_selection_categories__(db, query, as_dict):
    cur = db.cursor()
    selection_categories = []
    if as_dict:
        selection_categories = {}

    try:
        cur.execute(query)
        if as_dict:
            for (sc_id, sc_name) in cur:
                selection_categories[str(sc_id)] = {
                    "sc_id": str(sc_id),
                    "sc_name": str(sc_name)
                }
        else:
            for (sc_id, sc_name) in cur:
                selection_categories.append({
                    "sc_id": str(sc_id),
                    "sc_name": str(sc_name)
                })
    except Error as err:
        if 'Unknown column' in str(err):
            return INVALID_TYPE_EXCEPTION
        raise err
    finally:
        cur.close()
    return selection_categories


def get_selection_categories(db, as_dict = False):
    return __get_selection_categories__(db, get_queries["get_selection_categories"], as_dict)


def get_selection_category_end(db, as_dict = False):
    return __get_selection_categories__(db, get_queries["get_selection_category_end"], as_dict)


def get_selection_category_by_id(db, sc_id, as_dict = False):
    if sc_id == None:
        return EMPTY_INPUT_EXCEPTION
    return __get_selection_categories__(db, get_queries["get_selection_category_by_id"].replace("{sc_id}", str(sc_id)), as_dict)


def __get_selections__(db, query, as_dict):
    cur = db.cursor()
    selections = []
    if as_dict:
        selections = {}

    try:
        cur.execute(query)
        if as_dict:
            for (s_id, s_name, sc_id, i_id, s_price) in cur:
                selections[str(s_id)] = {
                    "s_id": str(s_id),
                    "s_name": str(s_name),
                    "sc_id": str(sc_id),
                    "i_id": str(i_id),
                    "s_price": str(s_price)
                }
        else:
            for (s_id, s_name, sc_id, i_id, s_price) in cur:
                selections.append({
                    "s_id": str(s_id),
                    "s_name": str(s_name),
                    "sc_id": str(sc_id),
                    "i_id": str(i_id),
                    "s_price": str(s_price)
                })    
        
        
    except Error as err:
        if 'Unknown column' in str(err):
            return INVALID_TYPE_EXCEPTION
        raise err
    finally:
        cur.close()

    return selections


def get_selections(db, as_dict = False):
    return __get_selections__(db, get_queries["get_selections"], as_dict)


def get_selection_end(db, as_dict = False):
    return __get_selections__(db, get_queries["get_selection_end"], as_dict)


def get_selection_by_id(db, s_id, as_dict = False):
    if s_id == None:
        return EMPTY_INPUT_EXCEPTION
    return __get_selections__(db, get_queries["get_selection_by_id"].replace("{s_id}", str(s_id)), as_dict)


def get_selections_by_course(db, c_id, as_dict = False):
    if c_id == None:
        return EMPTY_INPUT_EXCEPTION
    return __get_selections__(db, get_queries["get_selections_by_course"].replace("{c_id}", str(c_id)), as_dict)


def get_selections_by_ingredient(db, i_id, as_dict = False):
    if i_id == None:
        return EMPTY_INPUT_EXCEPTION
    return __get_selections__(db, get_queries["get_selections_by_ingredient"].replace("{i_id}", str(i_id)), as_dict)