from flask import render_template
from exceptions import *
import types
import mysql.connector
from mysql.connector import IntegrityError, DataError, Error

# Magnus Steinstø


insert_queries = {
    "insert_course": "INSERT INTO course (c_name, ca_id, info, price) VALUES ('{c_name}', '{ca_id}', '{info}', '{price}')",

    "insert_ingredient": "INSERT INTO ingredient (i_name, available) VALUES ('{i_name}', {available})",

    "insert_allergene": "INSERT INTO allergene (a_name) VALUES ('{a_name}')",

    "insert_category": "INSERT INTO category (ca_name) VALUES ('{ca_name}')",

    "insert_course_ingredient": "INSERT INTO course_ingredient (c_id, i_id) VALUES ({c_id}, {i_id})",

    "insert_selection_category": "INSERT INTO selection_category (sc_name) VALUES ('{sc_name}')",

    "insert_selection": "INSERT INTO selection (s_name, sc_id, i_id) VALUES ('{s_name}', '{sc_id}', '{i_id}')",

    "insert_course_selection": "INSERT INTO course_selection (c_id, s_id) VALUES ({c_id}, {s_id})",

    "insert_ingredient_allergene": "INSERT INTO ingredient_allergene (i_id, a_id) VALUES ({i_id}, {a_id})"
}

def insert_course(db, c_name, ca_id, info, price):
    cur = db.cursor()
    try:
        if c_name == None or ca_id == None or price == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(insert_queries["insert_course"].replace("{c_name}", c_name).replace("{ca_id}", str(ca_id)).replace("{info}", info).replace("{price}", str(price)))
        db.commit()
    except (IntegrityError) as err:
        if 'Cannot add or update a child row: a foreign key constraint fails' in str(err):
            return UNKKNOWN_REFERENCE_EXCEPTION
        return DUPLICATE_VALUE_EXCEPTION
    except (DataError):
        return INPUT_TOO_LONG_EXCEPTION
    except (Error) as err:
        if 'Incorrect decimal value' in str(err):
            return INVALID_DECIMAL_VALUE
        if 'Incorrect integer value' in str(err):
            return INVALID_TYPE_EXCEPTION

        raise err
    finally:
        cur.close()


def insert_ingredient(db, i_name, available):
    cur = db.cursor()
    try:
        if i_name == None or available == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(insert_queries["insert_ingredient"].replace("{i_name}", i_name).replace("{available}", str(available)))
        db.commit()
    except (IntegrityError):
        return DUPLICATE_VALUE_EXCEPTION
    except (DataError):
        return INPUT_TOO_LONG_EXCEPTION
    except Error as err:
        if 'Unknown column' in str(err):
            return INVALID_TYPE_EXCEPTION
        raise err
    finally:
        cur.close()


def insert_allergene(db, a_name):
    cur = db.cursor()
    try:
        if a_name == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(insert_queries["insert_allergene"].replace("{a_name}", a_name))
        db.commit()
    except (IntegrityError):
        return DUPLICATE_VALUE_EXCEPTION
    except (DataError):
        return INPUT_TOO_LONG_EXCEPTION
    finally:
        cur.close()


def insert_category(db, ca_name):
    cur = db.cursor()
    try:
        if ca_name == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(insert_queries["insert_category"].replace("{ca_name}", ca_name))
        db.commit()
    except (IntegrityError):
        return DUPLICATE_VALUE_EXCEPTION
    except (DataError):
        return INPUT_TOO_LONG_EXCEPTION
    finally:
        cur.close()


def insert_course_ingredient(db, c_id, i_id):
    cur = db.cursor()
    try:
        if c_id == None or i_id == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(insert_queries["insert_course_ingredient"].replace("{c_id}", str(c_id)).replace("{i_id}", str(i_id)))
        db.commit()
    except Error as err:
        if 'Cannot add or update a child row: a foreign key constraint fails' in str(err):
            return UNKKNOWN_REFERENCE_EXCEPTION
        if 'Unknown column' in str(err):
            return INVALID_TYPE_EXCEPTION
        raise err
    finally:
        cur.close()


def insert_selection_category(db, sc_name):
    cur = db.cursor()
    try:
        if sc_name == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(insert_queries["insert_selection_category"].replace("{sc_name}", sc_name))
        db.commit()
    except (IntegrityError):
        return DUPLICATE_VALUE_EXCEPTION
    except (DataError):
        return INPUT_TOO_LONG_EXCEPTION
    finally:
        cur.close()


def insert_selection(db, s_name, sc_id, i_id):
    cur = db.cursor()
    try:
        if s_name == None or sc_id == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(insert_queries["insert_selection"].replace("{s_name}", s_name).replace("{sc_id}", str(sc_id)).replace("{i_id}", str(i_id)))
        db.commit()
    except (IntegrityError) as err:
        if 'Cannot add or update a child row: a foreign key constraint fails' in str(err):
            return UNKKNOWN_REFERENCE_EXCEPTION
        return DUPLICATE_VALUE_EXCEPTION
    except (DataError):
        return INPUT_TOO_LONG_EXCEPTION
    except (Error) as err:
        if 'Incorrect integer value' in str(err):
            return INVALID_TYPE_EXCEPTION
        raise err
    finally:
        cur.close()


def insert_course_selection(db, c_id, s_id):
    cur = db.cursor()
    try:
        if c_id == None or s_id == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(insert_queries["insert_course_selection"].replace("{c_id}", str(c_id)).replace("{s_id}", str(s_id)))
        db.commit()
    except Error as err:
        if 'Cannot add or update a child row: a foreign key constraint fails' in str(err):
            return UNKKNOWN_REFERENCE_EXCEPTION
        if 'Unknown column' in str(err):
            return INVALID_TYPE_EXCEPTION
        raise err
    finally:
        cur.close()

    
def insert_ingredient_allergene(db, i_id, a_id):
    cur = db.cursor()
    try:
        if i_id == None or a_id == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(insert_queries["insert_ingredient_allergene"].replace("{i_id}", str(i_id)).replace("{a_id}", str(a_id)))
        db.commit()
    except Error as err:
        if 'Cannot add or update a child row: a foreign key constraint fails' in str(err):
            return UNKKNOWN_REFERENCE_EXCEPTION
        if 'Unknown column' in str(err):
            return INVALID_TYPE_EXCEPTION
        raise err
    finally:
        cur.close()