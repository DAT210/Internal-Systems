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

        # Check if value exists in the first place
        cur = db.cursor()
        try:
            cur.execute("SELECT c_id FROM course WHERE c_id = 1")
            value = cur.fetchone()[0]
        finally:
            cur.close()

        self.assertEqual(value, 1)

        # Check for course selection with the same c_id
        cur = db.cursor()
        course_selections = []

        try:
            cur.execute("SELECT c_id, s_id FROM course_selection WHERE c_id = 1")
            for (c_id, s_id) in cur:
                course_selections.append({
                    "c_id": str(c_id),
                    "s_id": str(s_id)
                })
        finally:
            cur.close()

        self.assertEqual(course_selections, [{'c_id': '1', 's_id': '1'}, {'c_id': '1', 's_id': '2'}])

        cur = db.cursor()
        course_ingredients = []

        try:
            cur.execute("SELECT c_id, i_id FROM course_ingredient WHERE c_id = 1")
            for (c_id, i_id) in cur:
                course_ingredients.append({
                    "c_id": str(c_id),
                    "i_id": str(i_id)
                })
        finally:
            cur.close()

        self.assertEqual(course_ingredients, [{'c_id': '1', 'i_id': '1'}, {'c_id': '1', 'i_id': '3'}])
        
        # Test valid remove 
        remove_course(db, 1)

        # Fetch the removed value
        cur = db.cursor()
        try:
            cur.execute("SELECT c_id FROM course WHERE c_id = 1")
            value = cur.fetchone()
        finally:
            cur.close()

        self.assertEqual(value, None)
        # Check for course selection with the same c_id
        cur = db.cursor()
        course_selections = []
        try:
            cur.execute("SELECT c_id, s_id FROM course_selection WHERE c_id = 1")
            for (c_id, s_id) in cur:
                course_selections.append({
                    "c_id": str(c_id),
                    "s_id": str(s_id)
                })
        finally:
            cur.close()
        self.assertEqual(course_selections, [])
        cur = db.cursor()
        course_ingredients = []
        try:
            cur.execute("SELECT c_id, i_id FROM course_ingredient WHERE c_id = 1")
            for (c_id, i_id) in cur:
                course_ingredients.append({
                    "c_id": str(c_id),
                    "i_id": str(i_id)
                })
        finally:
            cur.close()

        self.assertEqual(course_ingredients, [])

        # Remove with invalid id
        self.assertEqual(remove_course(db, "a"), 
                        INVALID_TYPE_EXCEPTION)

        # Remove with non-excisting id
        self.assertEqual(remove_course(db, 999), 
                        NO_UPDATE_EXCEPTION)
        db.close()


    def test_remove_ingredient(self):
        db = get_db()

        # Check if value exists in the first place
        """cur = db.cursor()
        try:
            cur.execute("SELECT i_id FROM ingredient WHERE i_id = 1")
            value = cur.fetchone()[0]
        finally:
            cur.close()

        self.assertEqual(value, 1)

        # Check for course selection with the i_id
        print("Course selections")
        cur = db.cursor()
        course_selections = []

        try:
            cur.execute("SELECT c_id, s.s_id FROM course_selection cs INNER JOIN selection AS s on s.s_id=cs.s_id WHERE i_id = 1")
            for (c_id, s_id) in cur:
                course_selections.append({
                    "c_id": str(c_id),
                    "s_id": str(s_id)
                })
        finally:
            cur.close()
        self.assertEqual(course_selections, [{'c_id': '3', 's_id': '3'}])

        # Check for selection with the i_id
        cur = db.cursor()
        selections = []

        try:
            cur.execute("SELECT sc_id, i_id FROM selection WHERE i_id = 1")
            for (sc_id, i_id) in cur:
                selections.append({
                    "sc_id": str(sc_id),
                    "i_id": str(i_id)
                })
        finally:
            cur.close()
        self.assertEqual(selections, [{'sc_id': '1', 'i_id': '1'}, {'sc_id': '1', 'i_id': '1'}])

        # Check for ingredient allergene
        cur = db.cursor()
        ingredient_allergenes = []

        try:
            cur.execute("SELECT i_id, a_id FROM ingredient_allergene WHERE i_id = 1")
            for (i_id, a_id) in cur:
                ingredient_allergenes.append({
                    "i_id": str(i_id),
                    "a_id": str(a_id)
                })
        finally:
            cur.close()
        self.assertEqual(ingredient_allergenes, [{'i_id': '1', 'a_id': '2'}, {'i_id': '1', 'a_id': '3'}])

        # Check for course ingredients
        cur = db.cursor()
        course_ingredients = []

        try:
            cur.execute("SELECT c_id, i_id FROM course_ingredient WHERE i_id = 1")
            for (c_id, i_id) in cur:
                course_ingredients.append({
                    "c_id": str(c_id),
                    "i_id": str(i_id)
                })
        finally:
            cur.close()
        self.assertEqual(course_ingredients, [{'c_id': '1', 'i_id': '1'}, {'c_id': '2', 'i_id': '1'}, {'c_id': '3', 'i_id': '1'}, {'c_id': '4', 'i_id': '1'}, {'c_id': '5', 'i_id': '1'}])
        
        print("Valid check")"""
        # Test valid remove 
        # remove_ingredient(db, 1)

        print("Removed")

        # Fetch the removed value
        """cur = db.cursor()
        try:
            cur.execute("SELECT c_id FROM course WHERE c_id = 1")
            value = cur.fetchone()
        except Error as err:
            return err
        finally:
            cur.close()

        self.assertEqual(value, None)
        # Check for course selection with the same c_id
        cur = db.cursor()
        course_selections = []
        try:
            cur.execute("SELECT c_id, s_id FROM course_selection WHERE c_id = 1")
            for (c_id, s_id) in cur:
                course_selections.append({
                    "c_id": str(c_id),
                    "s_id": str(s_id)
                })
        except Error as err:
            return err
        finally:
            cur.close()
        self.assertEqual(course_selections, [])
        cur = db.cursor()
        course_ingredients = []
        try:
            cur.execute("SELECT c_id, i_id FROM course_ingredient WHERE c_id = 1")
            for (c_id, i_id) in cur:
                course_ingredients.append({
                    "c_id": str(c_id),
                    "i_id": str(i_id)
                })
        except Error as err:
            return err
        finally:
            cur.close()

        self.assertEqual(course_ingredients, [])

        # Remove with invalid id
        self.assertEqual(remove_course(db, "a"), 
                        INVALID_TYPE_EXCEPTION)

        # Remove with non-excisting id
        self.assertEqual(remove_course(db, 999), 
                        NO_UPDATE_EXCEPTION)"""
        db.close()

    def test_remove_allergene(self):
        db = get_db()

        # Check if value exists in the first place
        cur = db.cursor()
        try:
            cur.execute("SELECT a_id FROM allergene WHERE a_id = 2")
            value = cur.fetchone()[0]
        finally:
            cur.close()

        self.assertEqual(value, 2)

        # Check for ingredient allergene with the same a_id
        cur = db.cursor()
        ingredient_allergenes = []

        try:
            cur.execute("SELECT i_id, a_id FROM ingredient_allergene WHERE a_id = 2")
            for (i_id, a_id) in cur:
                ingredient_allergenes.append({
                    "i_id": str(i_id),
                    "a_id": str(a_id)
                })
        finally:
            cur.close()

        self.assertEqual(ingredient_allergenes, [{'i_id': '1', 'a_id': '2'}])

        # Test valid remove 
        remove_allergene(db, 2)

        # Fetch the removed value
        cur = db.cursor()
        try:
            cur.execute("SELECT a_id FROM allergene WHERE a_id = 2")
            value = cur.fetchone()
        finally:
            cur.close()

        self.assertEqual(value, None)

        # Check for ingredient allergene with the same a_id
        cur = db.cursor()
        ingredient_allergenes = []

        try:
            cur.execute("SELECT i_id, a_id FROM ingredient_allergene WHERE a_id = 2")
            for (i_id, a_id) in cur:
                ingredient_allergenes.append({
                    "i_id": str(i_id),
                    "a_id": str(a_id)
                })
        finally:
            cur.close()

        self.assertEqual(ingredient_allergenes, [])

        # Remove with invalid id
        self.assertEqual(remove_allergene(db, "a"), 
                        INVALID_TYPE_EXCEPTION)

        # Remove with non-excisting id
        self.assertEqual(remove_allergene(db, 999), 
                        NO_UPDATE_EXCEPTION)
        db.close()


    def test_remove_course_ingredient(self):
        db = get_db()

        # Check if value exists in the first place
        cur = db.cursor()
        try:
            cur.execute("SELECT c_id FROM course_ingredient WHERE c_id=1 AND i_id=1")
            value = cur.fetchone()[0]
        finally:
            cur.close()

        self.assertEqual(value, 1)

        # Test valid remove 
        remove_course_ingredient(db, 1, 1)

        # Fetch the removed value
        cur = db.cursor()
        try:
            cur.execute("SELECT c_id FROM course_ingredient WHERE c_id=1 AND i_id=1")
            value = cur.fetchone()
        finally:
            cur.close()

        self.assertEqual(value, None)


        # Remove with invalid course id
        self.assertEqual(remove_course_ingredient(db, "a", 2), 
                        INVALID_TYPE_EXCEPTION)

        # Remove with non-excisting course id
        self.assertEqual(remove_course_ingredient(db, 999, 2), 
                        NO_UPDATE_EXCEPTION)

        # Remove with invalid ingredient id
        self.assertEqual(remove_course_ingredient(db, 2, "a"), 
                        INVALID_TYPE_EXCEPTION)

        # Remove with non-excisting ingredient id
        self.assertEqual(remove_course_ingredient(db, 2, 999), 
                        NO_UPDATE_EXCEPTION)
        
        db.close()


    def test_remove_course_selection(self):
        db = get_db()

        # Check if value exists in the first place
        cur = db.cursor()
        try:
            cur.execute("SELECT c_id FROM course_selection WHERE c_id=1 AND s_id=1")
            value = cur.fetchone()[0]
        finally:
            cur.close()

        self.assertEqual(value, 1)

        # Test valid remove 
        remove_course_selection(db, 1, 1)

        # Fetch the removed value
        cur = db.cursor()
        try:
            cur.execute("SELECT c_id FROM course_selection WHERE c_id=1 AND s_id=1")
            value = cur.fetchone()
        finally:
            cur.close()

        self.assertEqual(value, None)


        # Remove with invalid course id
        self.assertEqual(remove_course_selection(db, "a", 2), 
                        INVALID_TYPE_EXCEPTION)

        # Remove with non-excisting course id
        self.assertEqual(remove_course_selection(db, 999, 2), 
                        NO_UPDATE_EXCEPTION)

        # Remove with invalid selection id
        self.assertEqual(remove_course_selection(db, 2, "a"), 
                        INVALID_TYPE_EXCEPTION)

        # Remove with non-excisting selection id
        self.assertEqual(remove_course_selection(db, 2, 999), 
                        NO_UPDATE_EXCEPTION)
        
        db.close()


    def test_remove_ingredient_allergene(self):
        db = get_db()

        # Check if value exists in the first place
        cur = db.cursor()
        try:
            cur.execute("SELECT i_id FROM ingredient_allergene WHERE i_id=1 AND a_id=2")
            value = cur.fetchone()[0]
        finally:
            cur.close()

        self.assertEqual(value, 1)

        # Test valid remove 
        remove_ingredient_allergene(db, 1, 2)

        # Fetch the removed value
        cur = db.cursor()
        try:
            cur.execute("SELECT i_id FROM ingredient_allergene WHERE i_id=1 AND a_id=2")
            value = cur.fetchone()
        finally:
            cur.close()

        self.assertEqual(value, None)


        # Remove with invalid ingredient id
        self.assertEqual(remove_ingredient_allergene(db, "a", 3), 
                        INVALID_TYPE_EXCEPTION)

        # Remove with non-excisting ingredient id
        self.assertEqual(remove_ingredient_allergene(db, 999, 3), 
                        NO_UPDATE_EXCEPTION)

        # Remove with invalid allergene id
        self.assertEqual(remove_ingredient_allergene(db, 2, "a"), 
                        INVALID_TYPE_EXCEPTION)

        # Remove with non-excisting allergene id
        self.assertEqual(remove_ingredient_allergene(db, 2, 999), 
                        NO_UPDATE_EXCEPTION)
        
        db.close()


    """def test_remove_category(self):
        db = get_db()

        # Check if value exists in the first place
        cur = db.cursor()
        try:
            cur.execute("SELECT ca_id FROM category WHERE ca_id=1")
            value = cur.fetchone()[0]
        finally:
            cur.close()

        print(value)

        self.assertEqual(value, 1)

        # Test valid remove 
        remove_category(db, 1)

        # Fetch the removed value
        cur = db.cursor()
        try:
            cur.execute("SELECT ca_id FROM category WHERE ca_id=1")
            value = cur.fetchone()
        finally:
            cur.close()

        print(value)

        self.assertEqual(value, None)


        # Remove with invalid id
        self.assertEqual(remove_category(db, "a"), 
                        INVALID_TYPE_EXCEPTION)

        # Remove with non-excisting id
        self.assertEqual(remove_category(db, 999), 
                        NO_UPDATE_EXCEPTION)
        
        db.close()"""






if __name__ == '__main__':
    unittest.main()