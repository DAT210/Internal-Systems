import unittest
import update_functions
import get_functions
import test_database
import mysql.connector
from exceptions import *
from update_functions import *
from mysql.connector import errorcode, IntegrityError, DataError, Error

# Magnus Steinstø

def get_db():
    return mysql.connector.connect(user='root', password='root',
                                host='127.0.0.1',
                                database='test_menu')


class TestUpdateFunctions(unittest.TestCase):

    def setUp(self):
        # Called before each test
        test_database.create_test_db()


    def tearDown(self):
        # Called after every test
        test_database.drop_test_db()


    def test_update_course_name(self):
        db = get_db()
        # Valid input
        update_course_name(db, "update course alpha", 1)
        cur = db.cursor()
        try:
            cur.execute("SELECT c_name FROM course WHERE c_id=1")
            name = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()
        self.assertEqual("update course alpha", name)

        # Update name to existing name (name must be unique)
        self.assertEqual(update_course_name(db, "course charlie", 2),
                         DUPLICATE_VALUE_EXCEPTION)

        # Update name to invalid value
        self.assertEqual(update_course_name(db, "asdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf", 4),
                         INPUT_TOO_LONG_EXCEPTION)

        # Update name with non-existing id
        self.assertEqual(update_course_name(db, "course id out of bound", 999),
                         NO_UPDATE_EXCEPTION)

        # Update name to empty value
        self.assertEqual(update_course_name(db, None, 2),
                         EMPTY_INPUT_EXCEPTION)

        # Update name with empty id
        self.assertEqual(update_course_name(db, "valid input", None),
                         EMPTY_INPUT_EXCEPTION)

        db.close()

    def test_update_course_category(self):
        db = get_db()
        # Valid input
        update_course_category(db, 2, 1)
        cur = db.cursor()
        try:
            cur.execute("SELECT ca_id FROM course WHERE c_id=1")
            category = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()
        self.assertEqual(2, category)

        # Update category to invalid value
        self.assertEqual(update_course_category(db, "a", 3),
                         INVALID_TYPE_EXCEPTION)

        # Update category with non-existing id
        self.assertEqual(update_course_category(db, 3, 999),
                         NO_UPDATE_EXCEPTION)

        # Update to non-existing category
        self.assertEqual(update_course_category(db, 999, 2),
                         UNKKNOWN_REFERENCE_EXCEPTION)

        # Update category to empty value
        self.assertEqual(update_course_category(db, None, 4),
                         EMPTY_INPUT_EXCEPTION)

        # Update category with empty id
        self.assertEqual(update_course_category(db, 3, None),
                         EMPTY_INPUT_EXCEPTION)

        db.close()


    def test_update_course_info(self):
        db = get_db()
        # Valid input
        update_course_info(db, "update course alpha", 1)
        cur = db.cursor()
        try:
            cur.execute("SELECT info FROM course WHERE c_id=1")
            info = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()
        self.assertEqual("update course alpha", info)

        # Update info to invalid value
        self.assertEqual(update_course_info(db, "asdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf", 4),
                         INPUT_TOO_LONG_EXCEPTION)

        # Update info with non-existing id
        self.assertEqual(update_course_info(db, "course id out of bound", 999),
                         NO_UPDATE_EXCEPTION)

        # Update info to empty value
        self.assertEqual(update_course_info(db, None, 2),
                         EMPTY_INPUT_EXCEPTION)

        # Update info with empty id
        self.assertEqual(update_course_info(db, "valid input", None),
                         EMPTY_INPUT_EXCEPTION)

        db.close()


    def test_update_course_price(self):
        db = get_db()
        # Valid input
        update_functions.update_course_price(db, 5.55, 1)
        cur = db.cursor()
        try:
            cur.execute("SELECT price FROM course WHERE c_id=1")
            price = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()
        self.assertEqual(str(5.55), str(price))

        # Update price to invalid value
        self.assertEqual(update_course_price(db, "asdfasdfasd", 4),
                         INVALID_DECIMAL_VALUE)

        # Update price with non-existing id
        self.assertEqual(update_functions.update_course_price(db, 8.89, 999),
                         NO_UPDATE_EXCEPTION)

        # Update price to empty value
        self.assertEqual(update_functions.update_course_price(db, None, 2),
                         EMPTY_INPUT_EXCEPTION)

        # Update price with empty id
        self.assertEqual(update_functions.update_course_price(db, 4.34, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()

    def test_update_ingredient_name(self):
        db = get_db()
        # Valid input
        update_ingredient_name(db, "update ingredient alpha", 1)
        cur = db.cursor()
        try:
            cur.execute("SELECT i_name FROM ingredient WHERE i_id=1")
            name = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()
        self.assertEqual("update ingredient alpha", name)

        # Update name to existing name (name must be unique)
        self.assertEqual(update_ingredient_name(db, "ingredient charlie", 2),
                         DUPLICATE_VALUE_EXCEPTION)

        # Update name to invalid value
        self.assertEqual(update_ingredient_name(db, "asdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf", 4),
                         INPUT_TOO_LONG_EXCEPTION)

        # Update name with non-existing id
        self.assertEqual(update_ingredient_name(db, "course id out of bound", 999),
                         NO_UPDATE_EXCEPTION)

        # Update name to empty value
        self.assertEqual(update_ingredient_name(db, None, 2),
                         EMPTY_INPUT_EXCEPTION)

        # Update name with empty id
        self.assertEqual(update_ingredient_name(db, "valid input", None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_update_ingredient_availability(self):
        db = get_db()
        # Valid input
        update_ingredient_availability(db, False, 1)
        cur = db.cursor()
        try:
            cur.execute("SELECT available FROM ingredient WHERE i_id=1")
            available = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()
            
        self.assertEqual(0, available)

        # Update available to invalid value
        self.assertEqual(update_ingredient_availability(db, "a", 4),
                         INVALID_TYPE_EXCEPTION)

        # Update availability with non-existing id
        self.assertEqual(update_ingredient_availability(db, False, 999),
                         NO_UPDATE_EXCEPTION)

        # Update name to empty value
        self.assertEqual(update_ingredient_availability(db, None, 2),
                         EMPTY_INPUT_EXCEPTION)

        # Update name with empty id
        self.assertEqual(update_ingredient_availability(db, True, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_update_allergene_name(self):
        db = get_db()
        # Valid input
        update_allergene_name(db, "update allergene alpha", 1)
        cur = db.cursor()
        try:
            cur.execute("SELECT a_name FROM allergene WHERE a_id=1")
            name = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()
        self.assertEqual("update allergene alpha", name)

        # Update name to existing name (name must be unique)
        self.assertEqual(update_allergene_name(db, "allergene charlie", 2),
                         DUPLICATE_VALUE_EXCEPTION)

        # Update name to invalid value
        self.assertEqual(update_allergene_name(db, "asdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf", 4),
                         INPUT_TOO_LONG_EXCEPTION)

        # Update name with non-existing id
        self.assertEqual(update_allergene_name(db, "course id out of bound", 999),
                         NO_UPDATE_EXCEPTION)

        # Update name to empty value
        self.assertEqual(update_allergene_name(db, None, 2),
                         EMPTY_INPUT_EXCEPTION)

        # Update name with empty id
        self.assertEqual(update_allergene_name(db, "valid input", None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_update_category_name(self):
        db = get_db()
        # Valid input
        update_category_name(db, "update category alpha", 1)
        cur = db.cursor()
        try:
            cur.execute("SELECT ca_name FROM category WHERE ca_id=1")
            name = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()
        self.assertEqual("update category alpha", name)

        # Update name to existing name (name must be unique)
        self.assertEqual(update_category_name(db, "category charlie", 2),
                            DUPLICATE_VALUE_EXCEPTION)

        # Update name to invalid value
        self.assertEqual(update_category_name(db, "asdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf", 4),
                            INPUT_TOO_LONG_EXCEPTION)

        # Update name with non-existing id
        self.assertEqual(update_category_name(db, "category id out of bound", 999),
                            NO_UPDATE_EXCEPTION)

        # Update name to empty value
        self.assertEqual(update_category_name(db, None, 2),
                            EMPTY_INPUT_EXCEPTION)

        # Update name with empty id
        self.assertEqual(update_category_name(db, "valid input", None),
                            EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_update_selection_category_name(self):
        db = get_db()
        # Valid input
        update_selection_category_name(db, "update selection category alpha", 1)
        cur = db.cursor()
        try:
            cur.execute("SELECT sc_name FROM selection_category WHERE sc_id=1")
            name = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()
        self.assertEqual("update selection category alpha", name)

        # Update name to existing name (name must be unique)
        self.assertEqual(update_selection_category_name(db, "update selection category alpha", 2),
                            DUPLICATE_VALUE_EXCEPTION)

        # Update name to invalid value
        self.assertEqual(update_selection_category_name(db, "asdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfassdfasdfasdfasdfasfdasdfasdfasdfasdfasdfassdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfass", 2),
                            INPUT_TOO_LONG_EXCEPTION)

        # Update name with non-existing id
        self.assertEqual(update_selection_category_name(db, "selection category id out of bound", 999),
                            NO_UPDATE_EXCEPTION)

        # Update name to empty value
        self.assertEqual(update_selection_category_name(db, None, 2),
                            EMPTY_INPUT_EXCEPTION)

        # Update name with empty id
        self.assertEqual(update_selection_category_name(db, "valid input", None),
                            EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_update_selection_name(self):
        db = get_db()
        # Valid input
        update_selection_name(db, "update selection alpha", 1)
        cur = db.cursor()
        try:
            cur.execute("SELECT s_name FROM selection WHERE s_id=1")
            name = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()
        self.assertEqual("update selection alpha", name)

        # Update name to existing name (name must be unique)
        self.assertEqual(update_selection_name(db, "selection bravo", 3),
                            DUPLICATE_VALUE_EXCEPTION)

        # Update name to invalid value
        self.assertEqual(update_selection_name(db, "asdfasdfasdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf", 4),
                            INPUT_TOO_LONG_EXCEPTION)

        # Update name with non-existing id
        self.assertEqual(update_selection_name(db, "selection id out of bound", 999),
                            NO_UPDATE_EXCEPTION)

        # Update name to empty value
        self.assertEqual(update_selection_name(db, None, 2),
                            EMPTY_INPUT_EXCEPTION)

        # Update name with empty id
        self.assertEqual(update_selection_name(db, "valid input", None),
                            EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_update_selection_selection_category(self):
        db = get_db()
        # Valid input
        update_selection_selection_category(db, 2, 1)
        cur = db.cursor()
        try:
            cur.execute("SELECT sc_id FROM selection WHERE s_id=1")
            category = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()
        self.assertEqual(2, category)

        # Update category to invalid value
        self.assertEqual(update_selection_selection_category(db, "a", 3),
                         INVALID_TYPE_EXCEPTION)

        # Update category with non-existing id
        self.assertEqual(update_selection_selection_category(db, 3, 999),
                         NO_UPDATE_EXCEPTION)

        # Update to non-existing category
        self.assertEqual(update_selection_selection_category(db, 999, 2),
                         UNKKNOWN_REFERENCE_EXCEPTION)

        # Update category to empty value
        self.assertEqual(update_selection_selection_category(db, None, 4),
                         EMPTY_INPUT_EXCEPTION)

        # Update category with empty id
        self.assertEqual(update_selection_selection_category(db, 3, None),
                         EMPTY_INPUT_EXCEPTION)

        db.close()


    def test_update_selection_ingredient(self):
        db = get_db()
        # Valid input
        update_selection_ingredient(db, 2, 1)
        cur = db.cursor()
        try:
            cur.execute("SELECT i_id FROM selection WHERE s_id=1")
            ingredient = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()
        self.assertEqual(2, ingredient)

        # Update ingredient to invalid value
        self.assertEqual(update_selection_ingredient(db, "a", 3),
                         INVALID_TYPE_EXCEPTION)

        # Update ingredient with non-existing id
        self.assertEqual(update_selection_ingredient(db, 3, 999),
                         NO_UPDATE_EXCEPTION)

        # Update to non-existing ingredient
        self.assertEqual(update_selection_ingredient(db, 999, 2),
                         UNKKNOWN_REFERENCE_EXCEPTION)

        # Update ingredient to empty value
        self.assertEqual(update_selection_ingredient(db, None, 4),
                         EMPTY_INPUT_EXCEPTION)

        # Update ingredient with empty id
        self.assertEqual(update_selection_ingredient(db, 3, None),
                         EMPTY_INPUT_EXCEPTION)

        db.close()

    def test_update_selection_price(self):
        db = get_db()
        # Valid input
        update_functions.update_selection_price(db, 5.55, 1)
        cur = db.cursor()
        try:
            cur.execute("SELECT s_price FROM selection WHERE s_id=1")
            price = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()
        self.assertEqual(str(5.55), str(price))

        # Update price to invalid value
        self.assertEqual(update_selection_price(db, "asdfasdfasd", 4),
                         INVALID_DECIMAL_VALUE)

        # Update price with non-existing id
        self.assertEqual(update_selection_price(db, 8.89, 999),
                         NO_UPDATE_EXCEPTION)

        # Update price with empty id
        self.assertEqual(update_selection_price(db, 4.34, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


if __name__ == '__main__':
    unittest.main()


