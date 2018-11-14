import unittest
import update_functions
import get_functions
import test_database
import mysql.connector
from exceptions import *
from remove_functions import *
from mysql.connector import errorcode, IntegrityError, DataError, Error

# Magnus Steinstø

def get_db():
    return mysql.connector.connect(user='root', password='root',
                                host='127.0.0.1',
                                database='test_menu')


class TestRemoveFunctions(unittest.TestCase):

    def setUp(self):
        # Called before each test
        test_database.create_test_db()


    def tearDown(self):
        # Called after every test
        test_database.drop_test_db()


    def test_remove_course(self):
        db = get_db()

        cur = db.cursor()
        # Check if value exists in the first place
        try:
            cur.execute("SELECT c_id FROM course WHERE c_id = 2")
            value = cur.fetchone()[0]
        except Error as err:
            return err
        finally:
            cur.close()

        self.assertEqual(value, 2)
        
        # Test valid remove 
        remove_course(db, 2)

        # Fetch the removed value
        cur = db.cursor()
        try:
            cur.execute("SELECT c_id FROM course WHERE c_id = 2")
            value = cur.fetchone()
        except Error as err:
            return err
        finally:
            cur.close()

        self.assertEqual(value, None)

        # Remove with invalid id
        # self.assertEqual()

        """# Insert invalid name
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
                         EMPTY_INPUT_EXCEPTION)"""
        db.close()


if __name__ == '__main__':
    unittest.main()