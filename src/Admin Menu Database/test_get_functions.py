import unittest
import update_functions
import get_functions
import test_database
import mysql.connector
from exceptions import *
from get_functions import *
from mysql.connector import errorcode, IntegrityError, DataError, Error

# Magnus Steinstø

expected_return_values = {
    "get_courses": "[{'c_id': '1', 'c_name': 'course alpha', 'ca_id': '1', 'info': 'info alpha', 'price': '5.20', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': []}]}, {'c_id': '2', 'c_name': 'course bravo', 'ca_id': '2', 'info': 'info bravo', 'price': '4.20', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}]}, {'i_id': '2', 'i_name': 'ingredient bravo', 'available': '1', 'allergenes': [{'a_id': '3', 'a_name': 'allergene charlie'}]}, {'i_id': '5', 'i_name': 'ingredient echo', 'available': '1', 'allergenes': []}]}, {'c_id': '3', 'c_name': 'course charlie', 'ca_id': '1', 'info': 'info charlie', 'price': '3.75', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': []}]}, {'c_id': '4', 'c_name': 'course delta', 'ca_id': '3', 'info': 'info delta', 'price': '2.10', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}]}, {'i_id': '5', 'i_name': 'ingredient echo', 'available': '1', 'allergenes': []}]}, {'c_id': '5', 'c_name': 'course echo', 'ca_id': '4', 'info': 'info echo', 'price': '7.40', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}]}, {'i_id': '2', 'i_name': 'ingredient bravo', 'available': '1', 'allergenes': [{'a_id': '3', 'a_name': 'allergene charlie'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': []}]}]",
    "get_ingredients": "[{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}]}, {'i_id': '2', 'i_name': 'ingredient bravo', 'available': '1', 'allergenes': [{'a_id': '3', 'a_name': 'allergene charlie'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': []}, {'i_id': '4', 'i_name': 'ingredient delta', 'available': '1', 'allergenes': []}, {'i_id': '5', 'i_name': 'ingredient echo', 'available': '1', 'allergenes': []}]",
    "get_ingredients_by_course": "[{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': []}]",
    "get_allergens_by_ingredient": "[{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}]",
    "get_categories": "[{'ca_id': '1', 'ca_name': 'category alpha'}, {'ca_id': '2', 'ca_name': 'category bravo'}, {'ca_id': '3', 'ca_name': 'category charlie'}, {'ca_id': '4', 'ca_name': 'category delta'}]",
    "get_selection_categories": "[{'sc_id': '1', 'sc_name': 'selection category alpha'}, {'sc_id': '2', 'sc_name': 'selection category bravo'}]",
    "get_course_by_id": "('course alpha', 1, 'info alpha', Decimal('5.20'))",
    "get_selections": "[{'s_id': '1', 's_name': 'selection alpha', 'sc_id': '1', 'i_id': 'None'}, {'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2'}, {'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1'}, {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1'}]",
    "get_selections_by_course": "[{'s_id': '1', 's_name': 'selection alpha', 'sc_id': '1', 'i_id': 'None'}, {'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2'}]"
}

def get_db():
    return mysql.connector.connect(user='root', password='root',
                                host='127.0.0.1',
                                database='test_menu')


class TestGetFunctions(unittest.TestCase):

    def setUp(self):
        # Called before each test
        test_database.create_test_db()


    def tearDown(self):
        # Called after every test
        test_database.drop_test_db()

    def test_get_courses(self):
        db = get_db()

        # Get values and compare to expected results
        courses = get_courses(db)
        self.assertEqual(str(courses), expected_return_values["get_courses"])
        db.close()


    def test_get_ingredients(self):
        db = get_db()

        # Get values and compare to expected results
        ingredients = get_ingredients(db)
        self.assertEqual(str(ingredients), expected_return_values["get_ingredients"])
        db.close()

    
    def test_get_categories(self):
        db = get_db()

        # Get values and compare to expected results
        categories = get_categories(db)
        self.assertEqual(str(categories), expected_return_values["get_categories"])
        db.close()


    def test_get_selection_categories(self):
        db = get_db()

        # Get values and compare to expected results
        categories = get_selection_categories(db)
        self.assertEqual(str(categories), expected_return_values["get_selection_categories"])
        db.close()


    def test_get_selections(self):
        db = get_db()

        # Get values and compare to expected results
        selections = get_selections(db)
        self.assertEqual(str(selections), expected_return_values["get_selections"])
        db.close()

    def test_get_course_by_id(self):
        db = get_db()

        # Get value and compare to expected result
        course = get_course_by_id(db, 1)
        self.assertEqual(str(course), expected_return_values["get_course_by_id"])

        # Get with non-existing id (should return empty set)
        self.assertEqual(get_course_by_id(db, 999), None)

        # Get with invalid input id
        self.assertEqual(get_course_by_id(db, "a"),
                         INVALID_TYPE_EXCEPTION)

        # Get with empty id value
        self.assertEqual(get_course_by_id(db, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()



    def test_get_ingredients_by_course(self):
        db = get_db()

        # Get values and compare to expected results
        ingredients = get_ingredients_by_course(db, 1)
        self.assertEqual(str(ingredients), expected_return_values["get_ingredients_by_course"])

        # Get with non-existing id (should return empty set)
        self.assertEqual(get_ingredients_by_course(db, 999), [])

        # Get with invalid input id
        self.assertEqual(get_ingredients_by_course(db, "a"),
                         INVALID_TYPE_EXCEPTION)

        # Get with empty id value
        self.assertEqual(get_ingredients_by_course(db, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_get_allergenes_by_ingredient(self):
        db = get_db()

        # Get values and compare to expected results
        allergens = get_allergenes_by_ingredient(db, 1)
        self.assertEqual(str(allergens), expected_return_values["get_allergens_by_ingredient"])

        # Get with non-existing id (should return empty set)
        self.assertEqual(get_allergenes_by_ingredient(db, 999), [])

        # Get with invalid input id
        self.assertEqual(get_allergenes_by_ingredient(db, "a"),
                         INVALID_TYPE_EXCEPTION)

        # Get with empty id value
        self.assertEqual(get_allergenes_by_ingredient(db, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_get_selections_by_course(self):
        db = get_db()

        # Get values and compare to expected results
        selections = get_selections_by_course(db, 1)
        self.assertEqual(str(selections), expected_return_values["get_selections_by_course"])

        # Get with non-existing id (should return empty set)
        self.assertEqual(get_selections_by_course(db, 999), [])

        # Get with invalid input id
        self.assertEqual(get_selections_by_course(db, "a"),
                         INVALID_TYPE_EXCEPTION)

        # Get with empty id value
        self.assertEqual(get_selections_by_course(db, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


if __name__ == '__main__':
    unittest.main()
