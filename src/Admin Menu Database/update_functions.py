from flask import render_template
from exceptions import *
import types
import mysql.connector
from mysql.connector import IntegrityError, DataError, Error

# Magnus Steinstø

update_queries = {
    # ------------------------ Course ------------------------
    # Update course name by id
    "update_course_name": "UPDATE course SET c_name='{c_name}' WHERE c_id={c_id}",

    # Update course name by id
    "update_course_category": "UPDATE course SET ca_id='{ca_id}' WHERE c_id={c_id}",

    # Update course price by id
    "update_course_price": "UPDATE course SET price='{price}' WHERE c_id={c_id}",

    # ------------------------ Ingredient ------------------------
    # Update ingredient name by id
    "update_ingredient_name": "UPDATE ingredient SET i_name='{i_name}' WHERE i_id={i_id}",

    # Update ingredient availability by id
    "update_ingredient_availability": "UPDATE ingredient SET available={available} WHERE i_id={i_id}",

    # ------------------------ Allergene ------------------------
    # Update allergene name by id
    "update_allergene_name": "UPDATE allergene SET a_name='{a_name}' WHERE a_id={a_id}",
}

def update_course_name(db, c_name, c_id):
    cur = db.cursor()
    try:
        if c_name == None or c_id == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(update_queries["update_course_name"].replace("{c_name}", c_name).replace("{c_id}", str(c_id)))
        db.commit()
        if cur.rowcount == 0:
            return NO_UPDATE_EXCEPTION
    except (IntegrityError):
        return DUPLICATE_VALUE_EXCEPTION
    except (DataError):
        return INPUT_TOO_LONG_EXCEPTION

    finally:
        cur.close()


def update_course_category(db, ca_id, c_id):
    cur = db.cursor()
    try:
        if ca_id == None or c_id == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(update_queries["update_course_category"].replace("{ca_id}", str(ca_id)).replace("{c_id}", str(c_id)))
        db.commit()
        if cur.rowcount == 0:
            return NO_UPDATE_EXCEPTION
    except (Error) as err:
        if 'Incorrect integer value:' in str(err):
            return INVALID_TYPE_EXCEPTION
        if 'Cannot add or update a child row: a foreign key constraint fails' in str(err):
            return UNKKNOWN_REFERENCE_EXCEPTION
        print(str(err))
        raise err

    finally:
        cur.close()


def update_course_price(db, price, c_id):
    cur = db.cursor()
    try :
        if price == None or c_id == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(update_queries["update_course_price"].replace("{price}", str(price)).replace("{c_id}", str(c_id)))
        db.commit()
        if cur.rowcount == 0:
            return NO_UPDATE_EXCEPTION
    except (Error) as err:
        if 'Incorrect decimal value' in str(err):
            return INVALID_DECIMAL_VALUE
        raise err
    finally:
        cur.close()


def update_ingredient_name(db, i_name, i_id):
    cur = db.cursor()
    try:
        if i_name == None or i_id == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(update_queries["update_ingredient_name"].replace("{i_name}", i_name).replace("{i_id}", str(i_id)))
        db.commit()
        if cur.rowcount == 0:
            return NO_UPDATE_EXCEPTION
    except (IntegrityError):
        return DUPLICATE_VALUE_EXCEPTION
    except (DataError):
        return INPUT_TOO_LONG_EXCEPTION
    finally:
        cur.close()


def update_ingredient_availability(db, available, i_id):
    cur = db.cursor()
    try:
        if available == None or i_id == None:
            return EMPTY_INPUT_EXCEPTION
        if not (type(available) == bool):
            raise TypeError('Available is not of type boolean')
        cur.execute(
            update_queries["update_ingredient_availability"].replace("{available}", str(available)).replace("{i_id}",
                                                                                                            str(i_id)))
        db.commit()
        if cur.rowcount == 0:
            return NO_UPDATE_EXCEPTION
    except (TypeError):
        return INVALID_TYPE_EXCEPTION
    finally:
        cur.close()


def update_allergene_name(db, a_name, a_id):
    cur = db.cursor()
    try:
        if a_name == None or a_id == None:
            return EMPTY_INPUT_EXCEPTION
        cur.execute(update_queries["update_allergene_name"].replace("{a_name}", a_name).replace("{a_id}", str(a_id)))
        db.commit()
        if cur.rowcount == 0:
            return NO_UPDATE_EXCEPTION
    except (IntegrityError):
        return DUPLICATE_VALUE_EXCEPTION
    except (DataError):
        return INPUT_TOO_LONG_EXCEPTION
    finally:
        cur.close()