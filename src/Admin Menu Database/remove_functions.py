from flask import render_template
import mysql.connector

from exceptions import *

remove_queries = {
    # Delete a course by c_id
    "remove_course": ["DELETE FROM course_ingredient WHERE c_id = {c_id}", "DELETE FROM course WHERE c_id = {c_id}"],

    # Delete an ingredient by i_id
    "remove_ingredient": ["DELETE FROM course_ingredient WHERE i_id = {i_id}", "DELETE FROM ingredient_allergene WHERE i_id = {i_id}", "DELETE FROM ingredient WHERE i_id = {i_id}"],

    # Delete an allergene by a_id
    "remove_allergene": ["DELETE FROM ingredient_allergene WHERE a_id = {a_id}", "DELETE FROM allergene WHERE a_id = {a_id}"]
}


def remove_course(db, c_id):
    for q in remove_queries["remove_course"]:
        q = q.replace("{c_id}", str(c_id))
        execute_query(q, db)


def remove_ingredient(db, i_id):
    for q in remove_queries["remove_ingredient"]:
        q = q.replace("{i_id}", str(i_id))
        execute_query(q, db)


def remove_allergene(db, a_id):
    for q in remove_queries["remove_allergene"]:
        q = q.replace("{a_id}", str(a_id))
        execute_query(q, db)


def execute_query(query, db):
    cur = db.cursor()

    try:
        cur.execute(query)
        db.commit()
    except mysql.connector.Error as err:
        print(err)
        return render_template("error.html", msg=err)
    finally:
        cur.close()

