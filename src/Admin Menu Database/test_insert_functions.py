import unittest
import update_functions
import get_functions
import test_database
import mysql.connector
from exceptions import *
from insert_functions import *
from mysql.connector import errorcode, IntegrityError, DataError, Error

# Magnus Steinstø

def get_db():
    return mysql.connector.connect(user='root', password='root',
                                host='127.0.0.1',
                                database='test_menu')


class TestInsertFunctions(unittest.TestCase):

    def setUp(self):
        # Called before each test
        test_database.create_test_db()


    def tearDown(self):
        # Called after every test
        test_database.drop_test_db()


    def test_insert_course(self):
        db = get_db()
        # Valid input
        insert_course(db, "insert course", 2, "info insert course", 3.67)
        cur = db.cursor()
        try:
            cur.execute("SELECT c_name, ca_id, info, price FROM course WHERE c_id = (SELECT MAX(c_id) FROM course)")
            values = cur.fetchone()
            name = values[0]
            category = values[1]
            info = values[2]
            price = values[3]
        except Error as err:
            return err
        finally:
            cur.close()

        self.assertEqual(name, "insert course")
        self.assertEqual(category, 2)
        self.assertEqual(info, "info insert course")
        self.assertEqual(str(price), str(3.67))

        # Insert invalid name
        self.assertEqual(insert_course(db, "asdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf", 2, "info for course", 4.56),
                         INPUT_TOO_LONG_EXCEPTION)

        # Insert with invalid category
        self.assertEqual(insert_course(db, "course cat inv", "a", "info for course", 7.86),
                         INVALID_TYPE_EXCEPTION)

        # Insert invalid info
        self.assertEqual(insert_course(db, "course valid", 2, "asdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf", 4.56),
                         INPUT_TOO_LONG_EXCEPTION)

        # Insert invalid price
        self.assertEqual(insert_course(db, "course with valid name", 3, "info for course", "a"),
                         INVALID_DECIMAL_VALUE)

        # Insert name to existing name (name must be unique)
        self.assertEqual(insert_course(db, "course alpha", 4, "info for course", 2.13),
                         DUPLICATE_VALUE_EXCEPTION)

        # Insert category with non-existing id
        self.assertEqual(insert_course(db, "course cat none", 999, "info for course", 3.21),
                         UNKKNOWN_REFERENCE_EXCEPTION)

        # Insert with empty name value
        self.assertEqual(insert_course(db, None, 1, "info for course", 5.78),
                         EMPTY_INPUT_EXCEPTION)

        # Insert with empty category
        self.assertEqual(insert_course(db, "course cat empty", None, "info for course", 5.97),
                         EMPTY_INPUT_EXCEPTION)

        # Insert with empty price
        self.assertEqual(insert_course(db, "course unique name", 2, "info for course", None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_insert_ingredient(self):
        db = get_db()
        # Valid input
        insert_ingredient(db, "insert ingredient", False)
        cur = db.cursor()
        try:
            cur.execute("SELECT i_name, available FROM ingredient WHERE i_id = (SELECT MAX(i_id) FROM ingredient)")
            values = cur.fetchone()
            name = values[0]
            availability = values[1]
        except Error as err:
            return err
        finally:
            cur.close()

        self.assertEqual(name, "insert ingredient")
        self.assertEqual(availability, False)

        # Insert invalid name
        self.assertEqual(insert_ingredient(db,"asdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf", True),
                         INPUT_TOO_LONG_EXCEPTION)

        # Insert invalid availability
        self.assertEqual(insert_ingredient(db, "ingredient with valid name", "a"),
                         INVALID_TYPE_EXCEPTION)

        # Insert name to existing name (name must be unique)
        self.assertEqual(insert_ingredient(db, "ingredient alpha", True),
                         DUPLICATE_VALUE_EXCEPTION)

        # Insert with empty name value
        self.assertEqual(insert_ingredient(db, None, False),
                         EMPTY_INPUT_EXCEPTION)

        # Insert with empty availability
        self.assertEqual(insert_ingredient(db, "ingredient unique name", None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_insert_allergene(self):
        db = get_db()
        # Valid input
        insert_allergene(db, "insert allergene")
        cur = db.cursor()
        try:
            cur.execute("SELECT a_name FROM allergene WHERE a_id = (SELECT MAX(a_id) FROM allergene)")
            name = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()

        self.assertEqual(name, "insert allergene")

        # Insert invalid name
        self.assertEqual(insert_allergene(db, "asdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf"),
                         INPUT_TOO_LONG_EXCEPTION)

        # Insert name to existing name (name must be unique)
        self.assertEqual(insert_allergene(db, "allergene alpha"),
                         DUPLICATE_VALUE_EXCEPTION)

        # Insert with empty name value
        self.assertEqual(insert_allergene(db, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_insert_category(self):
        db = get_db()
        # Valid input
        insert_category(db, "insert category")
        cur = db.cursor()
        try:
            cur.execute("SELECT ca_name FROM category WHERE ca_id = (SELECT MAX(ca_id) FROM category)")
            category = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()

        self.assertEqual(category, "insert category")

        # Insert invalid name
        self.assertEqual(insert_category(db,
                                          "asdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf"),
                         INPUT_TOO_LONG_EXCEPTION)

        # Insert name to existing name (name must be unique)
        self.assertEqual(insert_category(db, "category alpha"),
                         DUPLICATE_VALUE_EXCEPTION)

        # Insert with empty name value
        self.assertEqual(insert_category(db, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_insert_course_ingredient(self):
        db = get_db()
        # Valid input
        insert_course_ingredient(db, 3, 2)
        cur = db.cursor()
        try:
            cur.execute("SELECT c_id, i_id FROM course_ingredient WHERE c_id = 3 AND i_id = 2")
            values = cur.fetchone()
            course = values[0]
            ingredient = values[1]
        except Error as err:
            return err
        finally:
            cur.close()

        self.assertEqual(course, 3)
        self.assertEqual(ingredient, 2)

        # Insert invalid course reference
        self.assertEqual(insert_course_ingredient(db, 999, 3),
                         UNKKNOWN_REFERENCE_EXCEPTION)

        # Insert invalid ingredient reference
        self.assertEqual(insert_course_ingredient(db, 5, 999),
                         UNKKNOWN_REFERENCE_EXCEPTION)

        # Insert invalid course value
        self.assertEqual(insert_course_ingredient(db, "a", 3),
                         INVALID_TYPE_EXCEPTION)

        # Insert invalid ingredient value
        self.assertEqual(insert_course_ingredient(db, 5, "a"),
                         INVALID_TYPE_EXCEPTION)

        # Insert with empty course value
        self.assertEqual(insert_course_ingredient(db, None, 3),
                         EMPTY_INPUT_EXCEPTION)

        # Insert with empty ingredient value
        self.assertEqual(insert_course_ingredient(db, 3, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_insert_selection_category(self):
        db = get_db()
        # Valid input
        insert_selection_category(db, "insert selection category")
        cur = db.cursor()
        try:
            cur.execute("SELECT sc_name FROM category WHERE sc_id = (SELECT MAX(sc_id) FROM category)")
            category = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()

        self.assertEqual(category, "insert selection category")

        # Insert invalid name
        self.assertEqual(insert_selection_category(db,
                                          "asdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf"),
                         INPUT_TOO_LONG_EXCEPTION)

        # Insert name to existing name (name must be unique)
        self.assertEqual(insert_selection_category(db, "selection category alpha"),
                         DUPLICATE_VALUE_EXCEPTION)

        # Insert with empty name value
        self.assertEqual(insert_selection_category(db, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_insert_selection(self):
        db = get_db()
        # Valid input
        insert_selection(db, "insert selection", 2, 2, 0.01)
        cur = db.cursor()
        try:
            cur.execute("SELECT s_name, sc_id, i_id, s_price FROM selection WHERE s_id = (SELECT MAX(s_id) FROM selection)")
            values = cur.fetchone()
            name = values[0]
            category = values[1]
            ingredient = values[2]
            price = values[3]
        except Error as err:
            return err
        finally:
            cur.close()

        self.assertEqual(name, "insert selection")
        self.assertEqual(category, 2)
        self.assertEqual(ingredient, 2)
        self.assertEqual(str(price), str(0.01))
        
        # Insert invalid name
        self.assertEqual(insert_selection(db, "asdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf", 1, 1, 3.39),
                         INPUT_TOO_LONG_EXCEPTION)

        # Insert with invalid category
        self.assertEqual(insert_selection(db, "selection cat inv", "a", 3, 7.65),
                         INVALID_TYPE_EXCEPTION)
        
        # Insert with invalid ingredient
        self.assertEqual(insert_selection(db, "selection cat inv", 2, "a", 4.43),
                         INVALID_TYPE_EXCEPTION)
        
        # Insert with invalid s_price
        self.assertEqual(insert_selection(db, "selection cat inv", 2, 3, "a"),
                         INVALID_DECIMAL_VALUE)
        
        # Insert name to existing name (name must be unique)
        self.assertEqual(insert_selection(db, "selection alpha", 1, 4, 2.15),
                         DUPLICATE_VALUE_EXCEPTION)

        # Insert category with non-existing selection category id
        self.assertEqual(insert_selection(db, "selection cat none", 999, 4, 2.34),
                         UNKKNOWN_REFERENCE_EXCEPTION)

        # Insert with empty name value
        self.assertEqual(insert_selection(db, None, 1, 3, 0.99),
                         EMPTY_INPUT_EXCEPTION)

        # Insert with empty category
        self.assertEqual(insert_selection(db, "selection cat empty", None, 3, 2.6),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_insert_course_selection(self):
        db = get_db()
        # Valid input
        insert_course_selection(db, 3, 2)
        cur = db.cursor()
        try:
            cur.execute("SELECT c_id, s_id FROM course_selection WHERE i_id = 3 AND a_id = 2")
            values = cur.fetchone()
            course = values[0]
            selection = values[1]
        except Error as err:
            return err
        finally:
            cur.close()

        self.assertEqual(course, 3)
        self.assertEqual(selection, 2)

        # Insert invalid course reference
        self.assertEqual(insert_course_selection(db, 999, 3),
                         UNKKNOWN_REFERENCE_EXCEPTION)

        # Insert invalid selection reference
        self.assertEqual(insert_course_selection(db, 3, 999),
                         UNKKNOWN_REFERENCE_EXCEPTION)

        # Insert invalid course value
        self.assertEqual(insert_course_selection(db, "a", 3),
                         INVALID_TYPE_EXCEPTION)

        # Insert invalid selection value
        self.assertEqual(insert_course_selection(db, 3, "a"),
                         INVALID_TYPE_EXCEPTION)

        # Insert with empty course value
        self.assertEqual(insert_course_selection(db, None, 3),
                         EMPTY_INPUT_EXCEPTION)

        # Insert with empty selection value
        self.assertEqual(insert_course_selection(db, 4, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_ingredient_allergene(self):
        db = get_db()
        # Valid input
        insert_ingredient_allergene(db, 3, 2)
        cur = db.cursor()
        try:
            cur.execute("SELECT i_id, a_id FROM ingredient_allergene WHERE i_id = 3 AND a_id = 2")
            values = cur.fetchone()
            ingredient = values[0]
            allergene = values[1]
        except Error as err:
            return err
        finally:
            cur.close()

        self.assertEqual(ingredient, 3)
        self.assertEqual(allergene, 2)

        # Insert invalid ingredient reference
        self.assertEqual(insert_ingredient_allergene(db, 999, 3),
                         UNKKNOWN_REFERENCE_EXCEPTION)

        # Insert invalid allergene reference
        self.assertEqual(insert_ingredient_allergene(db, 3, 999),
                         UNKKNOWN_REFERENCE_EXCEPTION)

        # Insert invalid ingredient value
        self.assertEqual(insert_ingredient_allergene(db, "a", 3),
                         INVALID_TYPE_EXCEPTION)

        # Insert invalid allergene value
        self.assertEqual(insert_ingredient_allergene(db, 3, "a"),
                         INVALID_TYPE_EXCEPTION)

        # Insert with empty ingredient value
        self.assertEqual(insert_ingredient_allergene(db, None, 3),
                         EMPTY_INPUT_EXCEPTION)

        # Insert with empty allergene value
        self.assertEqual(insert_ingredient_allergene(db, 4, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


if __name__ == '__main__':
    unittest.main()