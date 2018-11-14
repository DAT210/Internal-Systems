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
    "get_courses": "[{'c_id': '1', 'c_name': 'course alpha', 'ca_id': '1', 'info': 'info alpha', 'price': '5.20', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}, {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1', 's_price': '1.26'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': [], 'selections': []}], 'selections': [{'s_id': '1', 's_name': 'selection alpha', 'sc_id': '1', 'i_id': 'None', 's_price': 'None'}, {'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}]}, {'c_id': '2', 'c_name': 'course bravo', 'ca_id': '2', 'info': 'info bravo', 'price': '4.20', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}, {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1', 's_price': '1.26'}]}, {'i_id': '2', 'i_name': 'ingredient bravo', 'available': '1', 'allergenes': [{'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}]}, {'i_id': '5', 'i_name': 'ingredient echo', 'available': '1', 'allergenes': [], 'selections': []}], 'selections': [{'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}]}, {'c_id': '3', 'c_name': 'course charlie', 'ca_id': '1', 'info': 'info charlie', 'price': '3.75', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}, {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1', 's_price': '1.26'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': [], 'selections': []}], 'selections': [{'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}]}, {'c_id': '4', 'c_name': 'course delta', 'ca_id': '3', 'info': 'info delta', 'price': '2.10', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}, {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1', 's_price': '1.26'}]}, {'i_id': '5', 'i_name': 'ingredient echo', 'available': '1', 'allergenes': [], 'selections': []}], 'selections': [{'s_id': '1', 's_name': 'selection alpha', 'sc_id': '1', 'i_id': 'None', 's_price': 'None'}, {'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}]}, {'c_id': '5', 'c_name': 'course echo', 'ca_id': '4', 'info': 'info echo', 'price': '7.40', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}, {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1', 's_price': '1.26'}]}, {'i_id': '2', 'i_name': 'ingredient bravo', 'available': '1', 'allergenes': [{'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': [], 'selections': []}], 'selections': []}]",
    "get_course_end": "[{'c_id': '5', 'c_name': 'course echo', 'ca_id': '4', 'info': 'info echo', 'price': '7.40', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}, {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1', 's_price': '1.26'}]}, {'i_id': '2', 'i_name': 'ingredient bravo', 'available': '1', 'allergenes': [{'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': [], 'selections': []}], 'selections': []}]",
    "get_courses_id_name": "[{'c_id': '1', 'c_name': 'course alpha'}, {'c_id': '2', 'c_name': 'course bravo'}, {'c_id': '3', 'c_name': 'course charlie'}, {'c_id': '4', 'c_name': 'course delta'}, {'c_id': '5', 'c_name': 'course echo'}]",
    "get_ingredients": "[{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}, {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1', 's_price': '1.26'}]}, {'i_id': '2', 'i_name': 'ingredient bravo', 'available': '1', 'allergenes': [{'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': [], 'selections': []}, {'i_id': '4', 'i_name': 'ingredient delta', 'available': '1', 'allergenes': [], 'selections': []}, {'i_id': '5', 'i_name': 'ingredient echo', 'available': '1', 'allergenes': [], 'selections': []}]",
    "get_ingredient_end": "[{'i_id': '5', 'i_name': 'ingredient echo', 'available': '1', 'allergenes': [], 'selections': []}]",
    "get_ingredients_by_course": "[{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}, {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1', 's_price': '1.26'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': [], 'selections': []}]",
    "get_allergenes": "[{'a_id': '1', 'a_name': 'allergene alpha'}, {'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}, {'a_id': '4', 'a_name': 'allergene delta'}, {'a_id': '5', 'a_name': 'allergene echo'}]",
    "get_allergene_end": "[{'a_id': '5', 'a_name': 'allergene echo'}]",
    "get_allergene_by_id": "[{'a_id': '1', 'a_name': 'allergene alpha'}]",
    "get_allergens_by_ingredient": "[{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}]",
    "get_categories": "[{'ca_id': '1', 'ca_name': 'category alpha'}, {'ca_id': '2', 'ca_name': 'category bravo'}, {'ca_id': '3', 'ca_name': 'category charlie'}, {'ca_id': '4', 'ca_name': 'category delta'}]",
    "get_category_end": "[{'ca_id': '4', 'ca_name': 'category delta'}]",
    "get_category_by_id": "[{'ca_id': '1', 'ca_name': 'category alpha'}]",
    "get_selection_categories": "[{'sc_id': '1', 'sc_name': 'selection category alpha'}, {'sc_id': '2', 'sc_name': 'selection category bravo'}]",
    "get_selection_category_end": "[{'sc_id': '2', 'sc_name': 'selection category bravo'}]",
    "get_selection_category_by_id": "[{'sc_id': '1', 'sc_name': 'selection category alpha'}]",
    "get_course_by_id": "[{'c_id': '1', 'c_name': 'course alpha', 'ca_id': '1', 'info': 'info alpha', 'price': '5.20', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}, {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1', 's_price': '1.26'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': [], 'selections': []}], 'selections': [{'s_id': '1', 's_name': 'selection alpha', 'sc_id': '1', 'i_id': 'None', 's_price': 'None'}, {'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}]}]",
    "get_selections": "[{'s_id': '1', 's_name': 'selection alpha', 'sc_id': '1', 'i_id': 'None', 's_price': 'None'}, {'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}, {'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}, {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1', 's_price': '1.26'}]",
    "get_selection_end": "[{'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}]",
    "get_selection_by_id": "[{'s_id': '1', 's_name': 'selection alpha', 'sc_id': '1', 'i_id': 'None', 's_price': 'None'}]",
    "get_selections_by_course": "[{'s_id': '1', 's_name': 'selection alpha', 'sc_id': '1', 'i_id': 'None', 's_price': 'None'}, {'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}]"
}

expected_return_dictionary = {
    "get_allergenes_by_ingredient": {'2': {'a_id': '2', 'a_name': 'allergene bravo'}, '3': {'a_id': '3', 'a_name': 'allergene charlie'}},
    "get_categories": {'1': {'ca_id': '1', 'ca_name': 'category alpha'}, '2': {'ca_id': '2', 'ca_name': 'category bravo'}, '3': {'ca_id': '3', 'ca_name': 'category charlie'}, '4': {'ca_id': '4', 'ca_name': 'category delta'}},
    "get_category_end": {'4': {'ca_id': '4', 'ca_name': 'category delta'}},
    "get_category_by_id": {'1': {'ca_id': '1', 'ca_name': 'category alpha'}},
    "get_course_by_id": {'1': {'c_id': '1', 'c_name': 'course alpha', 'ca_id': '1', 'info': 'info alpha', 'price': '5.20', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}, {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1', 's_price': '1.26'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': [], 'selections': []}], 'selections': [{'s_id': '1', 's_name': 'selection alpha', 'sc_id': '1', 'i_id': 'None', 's_price': 'None'}, {'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}]}},
    "get_courses": {'1': {'c_id': '1', 'c_name': 'course alpha', 'ca_id': '1', 'info': 'info alpha', 'price': '5.20', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}, {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1', 's_price': '1.26'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': [], 'selections': []}], 'selections': [{'s_id': '1', 's_name': 'selection alpha', 'sc_id': '1', 'i_id': 'None', 's_price': 'None'}, {'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}]}, '2': {'c_id': '2', 'c_name': 'course bravo', 'ca_id': '2', 'info': 'info bravo', 'price': '4.20', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}, {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1', 's_price': '1.26'}]}, {'i_id': '2', 'i_name': 'ingredient bravo', 'available': '1', 'allergenes': [{'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}]}, {'i_id': '5', 'i_name': 'ingredient echo', 'available': '1', 'allergenes': [], 'selections': []}], 'selections': [{'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}]}, '3': {'c_id': '3', 'c_name': 'course charlie', 'ca_id': '1', 'info': 'info charlie', 'price': '3.75', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}, {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1', 's_price': '1.26'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': [], 'selections': []}], 'selections': [{'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}]}, '4': {'c_id': '4', 'c_name': 'course delta', 'ca_id': '3', 'info': 'info delta', 'price': '2.10', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}, {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1', 's_price': '1.26'}]}, {'i_id': '5', 'i_name': 'ingredient echo', 'available': '1', 'allergenes': [], 'selections': []}], 'selections': [{'s_id': '1', 's_name': 'selection alpha', 'sc_id': '1', 'i_id': 'None', 's_price': 'None'}, {'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}]}, '5': {'c_id': '5', 'c_name': 'course echo', 'ca_id': '4', 'info': 'info echo', 'price': '7.40', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}, {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1', 's_price': '1.26'}]}, {'i_id': '2', 'i_name': 'ingredient bravo', 'available': '1', 'allergenes': [{'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': [], 'selections': []}], 'selections': []}},
    "get_course_end": {'5': {'c_id': '5', 'c_name': 'course echo', 'ca_id': '4', 'info': 'info echo', 'price': '7.40', 'ingredients': [{'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}, {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1', 's_price': '1.26'}]}, {'i_id': '2', 'i_name': 'ingredient bravo', 'available': '1', 'allergenes': [{'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}]}, {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': [], 'selections': []}], 'selections': []}},
    "get_courses_id_name": {'1': {'c_id': '1', 'c_name': 'course alpha'}, '2': {'c_id': '2', 'c_name': 'course bravo'}, '3': {'c_id': '3', 'c_name': 'course charlie'}, '4': {'c_id': '4', 'c_name': 'course delta'}, '5': {'c_id': '5', 'c_name': 'course echo'}},
    "get_ingredients": {'1': {'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}, {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1', 's_price': '1.26'}]}, '2': {'i_id': '2', 'i_name': 'ingredient bravo', 'available': '1', 'allergenes': [{'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}]}, '3': {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': [], 'selections': []}, '4': {'i_id': '4', 'i_name': 'ingredient delta', 'available': '1', 'allergenes': [], 'selections': []}, '5': {'i_id': '5', 'i_name': 'ingredient echo', 'available': '1', 'allergenes': [], 'selections': []}},
    "get_ingredient_end": {'5': {'i_id': '5', 'i_name': 'ingredient echo', 'available': '1', 'allergenes': [], 'selections': []}},
    "get_allergene_by_id": {'1': {'a_id': '1', 'a_name': 'allergene alpha'}},
    "get_ingredients_by_course": {'1': {'i_id': '1', 'i_name': 'ingredient alpha', 'available': '1', 'allergenes': [{'a_id': '2', 'a_name': 'allergene bravo'}, {'a_id': '3', 'a_name': 'allergene charlie'}], 'selections': [{'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}, {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1', 's_price': '1.26'}]}, '3': {'i_id': '3', 'i_name': 'ingredient charlie', 'available': '1', 'allergenes': [], 'selections': []}},
    "get_allergenes": {'1': {'a_id': '1', 'a_name': 'allergene alpha'}, '2': {'a_id': '2', 'a_name': 'allergene bravo'}, '3': {'a_id': '3', 'a_name': 'allergene charlie'}, '4': {'a_id': '4', 'a_name': 'allergene delta'}, '5': {'a_id': '5', 'a_name': 'allergene echo'}},
    "get_allergene_end": {'5': {'a_id': '5', 'a_name': 'allergene echo'}},
    "get_selections": {'1': {'s_id': '1', 's_name': 'selection alpha', 'sc_id': '1', 'i_id': 'None', 's_price': 'None'}, '2': {'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}, '3': {'s_id': '3', 's_name': 'selection charlie', 'sc_id': '1', 'i_id': '1', 's_price': '2.16'}, '4': {'s_id': '4', 's_name': 'selection delta', 'sc_id': '1', 'i_id': '1', 's_price': '1.26'}},
    "get_selection_end": {'2': {'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}},
    "get_selection_by_id": {'1': {'s_id': '1', 's_name': 'selection alpha', 'sc_id': '1', 'i_id': 'None', 's_price': 'None'}},
    "get_selection_categories": {'1': {'sc_id': '1', 'sc_name': 'selection category alpha'}, '2': {'sc_id': '2', 'sc_name': 'selection category bravo'}},
    "get_selection_category_end": {'2': {'sc_id': '2', 'sc_name': 'selection category bravo'}},
    "get_selection_category_by_id": {'1': {'sc_id': '1', 'sc_name': 'selection category alpha'}},
    "get_selections_by_course": {'1': {'s_id': '1', 's_name': 'selection alpha', 'sc_id': '1', 'i_id': 'None', 's_price': 'None'}, '2': {'s_id': '2', 's_name': 'selection bravo', 'sc_id': '2', 'i_id': '2', 's_price': '4.56'}}
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

        # Get values and compare to expected results (list)
        courses = get_courses(db)
        self.assertEqual(str(courses), expected_return_values["get_courses"])

        # Get values and compare to expected results (dictionary)
        courses = get_courses(db, True)
        self.assertEqual(courses, expected_return_dictionary["get_courses"])

        db.close()

    def test_course_end(self):
        db = get_db()

        # Get value and compare to expected results (list)
        course = get_course_end(db)
        self.assertEqual(str(course), expected_return_values["get_course_end"])

        # Get values and compare to expected results (dictionary)
        course = get_course_end(db, True)
        self.assertEqual(course, expected_return_dictionary["get_course_end"])

        db.close()


    def test_get_courses_id_name(self):
        db = get_db()

        # Get value and compare to expected results (list)
        courses = get_courses_id_name(db)
        self.assertEqual(str(courses), expected_return_values["get_courses_id_name"])

        # Get values and compare to expected results (dictionary)
        courses = get_courses_id_name(db, True)
        self.assertEqual(courses, expected_return_dictionary["get_courses_id_name"])

        db.close()


    def test_get_ingredients(self):
        db = get_db()

        # Get values and compare to expected results (list)
        ingredients = get_ingredients(db)
        self.assertEqual(str(ingredients), expected_return_values["get_ingredients"])

        # Get values and compare to expected results (dictionary)
        ingredients = get_ingredients(db, True)
        self.assertEqual(ingredients, expected_return_dictionary["get_ingredients"])

        db.close()

    def test_get_ingredient_end(self):
        db = get_db()

        # Get values and compare to expected results (list)
        ingredient = get_ingredient_end(db)
        self.assertEqual(str(ingredient), expected_return_values["get_ingredient_end"])

        # Get values and compare to expected results (dictionary)
        ingredient = get_ingredient_end(db, True)
        self.assertEqual(ingredient, expected_return_dictionary["get_ingredient_end"])

        db.close()

    
    def test_get_categories(self):
        db = get_db()

        # Get values and compare to expected results (list)
        categories = get_categories(db)
        self.assertEqual(str(categories), expected_return_values["get_categories"])

        # Get values and compare to expected results (dictionary)
        categories = get_categories(db, True)
        self.assertEqual(categories, expected_return_dictionary["get_categories"])
        db.close()


    def test_get_category_end(self):
        db = get_db()

        # Get values and compare to expected results (list)
        category = get_category_end(db)
        self.assertEqual(str(category), expected_return_values["get_category_end"])

        # Get values and compare to expected results (dictionary)
        category = get_category_end(db, True)
        self.assertEqual(category, expected_return_dictionary["get_category_end"])
        
        db.close()


    def test_get_category_by_id(self):
        db = get_db()

        # Get value and compare to expected result (list)
        category = get_category_by_id(db, 1)
        self.assertEqual(str(category), expected_return_values["get_category_by_id"])

        # Get value and compare to expected result (dictionary)
        category = get_category_by_id(db, 1, True)
        self.assertEqual(category, expected_return_dictionary["get_category_by_id"])

        # Get with non-existing id (should return empty set)
        self.assertEqual(get_category_by_id(db, 999), [])

        # Get with invalid input id
        self.assertEqual(get_category_by_id(db, "a"),
                         INVALID_TYPE_EXCEPTION)

        # Get with empty id value
        self.assertEqual(get_category_by_id(db, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()



    def test_get_selection_categories(self):
        db = get_db()

        # Get values and compare to expected results (list)
        categories = get_selection_categories(db)
        self.assertEqual(str(categories), expected_return_values["get_selection_categories"])

        # Get values and compare to expected results (dictionary)
        categories = get_selection_categories(db, True)
        self.assertEqual(categories, expected_return_dictionary["get_selection_categories"])

        db.close()


    def test_get_selection_category_end(self):
        db = get_db()

        # Get values and compare to expected results (list)
        selection_category = get_selection_category_end(db)
        self.assertEqual(str(selection_category), expected_return_values["get_selection_category_end"])

        # Get values and compare to expected results (dictionary)
        selection_category = get_selection_category_end(db, True)
        self.assertEqual(selection_category, expected_return_dictionary["get_selection_category_end"])

        db.close()

    def test_get_selection_category_by_id(self):
        db = get_db()

        # Get value and compare to expected result (list)
        selection_category = get_selection_category_by_id(db, 1)
        self.assertEqual(str(selection_category), expected_return_values["get_selection_category_by_id"])

        # Get value and compare to expected result (dictionary)
        selection_category = get_selection_category_by_id(db, 1, True)
        self.assertEqual(selection_category, expected_return_dictionary["get_selection_category_by_id"])

        # Get with non-existing id (should return empty set)
        self.assertEqual(get_selection_category_by_id(db, 999), [])

        # Get with invalid input id
        self.assertEqual(get_selection_category_by_id(db, "a"),
                         INVALID_TYPE_EXCEPTION)

        # Get with empty id value
        self.assertEqual(get_selection_category_by_id(db, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()



    def test_get_selections(self):
        db = get_db()

        # Get values and compare to expected results (list)
        selections = get_selections(db)
        self.assertEqual(str(selections), expected_return_values["get_selections"])

        # Get values and compare to expected results (dictionary)
        selections = get_selections(db, True)
        self.assertEqual(selections, expected_return_dictionary["get_selections"])

        db.close()

    def test_get_selection_end(self):
        db = get_db()

        # Get values and compare to expected results (list)
        selection = get_selection_end(db)
        self.assertEqual(str(selection), expected_return_values["get_selection_end"])

        # Get values and compare to expected results (dictionary)
        selection = get_selection_end(db, True)
        self.assertEqual(selection, expected_return_dictionary["get_selection_end"])

        db.close()

    def test_get_selection_by_id(self):
        db = get_db()

        # Get value and compare to expected result (list)
        selection = get_selection_by_id(db, 1)
        self.assertEqual(str(selection), expected_return_values["get_selection_by_id"])

        # Get value and compare to expected result (dictionary)
        selection = get_selection_by_id(db, 1, True)
        self.assertEqual(selection, expected_return_dictionary["get_selection_by_id"])

        # Get with non-existing id (should return empty set)
        self.assertEqual(get_selection_by_id(db, 999), [])

        # Get with invalid input id
        self.assertEqual(get_selection_by_id(db, "a"),
                         INVALID_TYPE_EXCEPTION)

        # Get with empty id value
        self.assertEqual(get_selection_by_id(db, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_get_selections_by_course(self):
        db = get_db()

        # Get values and compare to expected results (list)
        selections = get_selections_by_course(db, 1)
        self.assertEqual(str(selections), expected_return_values["get_selections_by_course"])

        # Get values and compare to expected results (dictionary)
        selections = get_selections_by_course(db, 1, True)
        self.assertEqual(selections, expected_return_dictionary["get_selections_by_course"])

        # Get with non-existing id (should return empty set)
        self.assertEqual(get_selections_by_course(db, 999), [])

        # Get with invalid input id
        self.assertEqual(get_selections_by_course(db, "a"),
                         INVALID_TYPE_EXCEPTION)

        # Get with empty id value
        self.assertEqual(get_selections_by_course(db, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()




    def test_get_course_by_id(self):
        db = get_db()

        # Get value and compare to expected result (list)
        course = get_course_by_id(db, 1)
        self.assertEqual(str(course), expected_return_values["get_course_by_id"])

        # Get value and compare to expected result (dictionary)
        course = get_course_by_id(db, 1, True)
        self.assertEqual(course, expected_return_dictionary["get_course_by_id"])

        # Get with non-existing id (should return empty set)
        self.assertEqual(get_course_by_id(db, 999), [])

        # Get with invalid input id
        self.assertEqual(get_course_by_id(db, "a"),
                         INVALID_TYPE_EXCEPTION)

        # Get with empty id value
        self.assertEqual(get_course_by_id(db, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()



    def test_get_ingredients_by_course(self):
        db = get_db()

        # Get values and compare to expected results (list)
        ingredients = get_ingredients_by_course(db, 1)
        self.assertEqual(str(ingredients), expected_return_values["get_ingredients_by_course"])

        # Get values and compare to expected results (dictionary)
        ingredients = get_ingredients_by_course(db, 1, True)
        self.assertEqual(ingredients, expected_return_dictionary["get_ingredients_by_course"])

        # Get with non-existing id (should return empty set)
        self.assertEqual(get_ingredients_by_course(db, 999), [])

        # Get with invalid input id
        self.assertEqual(get_ingredients_by_course(db, "a"),
                         INVALID_TYPE_EXCEPTION)

        # Get with empty id value
        self.assertEqual(get_ingredients_by_course(db, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_get_get_allergenes(self):
        db = get_db()

        # Get values and compare to expected results (list)
        allergenes = get_allergenes(db)
        self.assertEqual(str(allergenes), expected_return_values["get_allergenes"])

        # Get values and compare to expected results (dictionary)
        allergenes = get_allergenes(db, True)
        self.assertEqual(allergenes, expected_return_dictionary["get_allergenes"])

        db.close()


    def test_get_allergenes_end(self):
        db = get_db()

        # Get values and compare to expected results (list)
        allergene = get_allergene_end(db)
        self.assertEqual(str(allergene), expected_return_values["get_allergene_end"])

        # Get values and compare to expected results (dictionary)
        allergene = get_allergene_end(db, True)
        self.assertEqual(allergene, expected_return_dictionary["get_allergene_end"])

        db.close()


    def test_get_allergene_by_id(self):
        db = get_db()

        # Get values and compare to expected results (list)
        allergene = get_allergene_by_id(db, 1)
        self.assertEqual(str(allergene), expected_return_values["get_allergene_by_id"])

        # Get values and compare to expected results (dictionary)
        allergene = get_allergene_by_id(db, 1, True)
        self.assertEqual(allergene, expected_return_dictionary["get_allergene_by_id"])
        
        # Get with non-existing id (should return empty set)
        self.assertEqual(get_allergene_by_id(db, 999), [])
        
        # Get with invalid input id
        self.assertEqual(get_allergene_by_id(db, "a"),
                         INVALID_TYPE_EXCEPTION)

        # Get with empty id value
        self.assertEqual(get_allergene_by_id(db, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()


    def test_get_allergenes_by_ingredient(self):
        db = get_db()

        # Get values and compare to expected results (list)
        allergens = get_allergenes_by_ingredient(db, 1)
        self.assertEqual(str(allergens), expected_return_values["get_allergens_by_ingredient"])

        # Get values and compare to expected results (dictionary)
        allergens = get_allergenes_by_ingredient(db, 1, True)
        self.assertEqual(allergens, expected_return_dictionary["get_allergenes_by_ingredient"])
        
        # Get with non-existing id (should return empty set)
        self.assertEqual(get_allergenes_by_ingredient(db, 999), [])
        

        # Get with invalid input id
        self.assertEqual(get_allergenes_by_ingredient(db, "a"),
                         INVALID_TYPE_EXCEPTION)

        # Get with empty id value
        self.assertEqual(get_allergenes_by_ingredient(db, None),
                         EMPTY_INPUT_EXCEPTION)
        db.close()

if __name__ == '__main__':
    unittest.main()
