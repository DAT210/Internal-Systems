import mysql.connector

username = "root"
password = "root"
database = "test_menu"


def create_test_db():
  create_db = mysql.connector.connect(
    host="localhost",
    user=username,
    passwd=password
  )
  create_cursor = create_db.cursor()
  # Create the database itself
  create_cursor.execute("DROP DATABASE IF EXISTS " + database)
  create_cursor.execute("CREATE DATABASE test_menu")

  create_db.close()
  # Connect to the newly created database
  db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database=database
  )
  cursor = db.cursor()

  # Insert further queries into the newly created database
  table_queries = [
    "CREATE TABLE ingredient (i_id INT(6) AUTO_INCREMENT,i_name VARCHAR(64) NOT NULL UNIQUE, available BOOLEAN, PRIMARY KEY (i_id))",
    "CREATE TABLE allergene (a_id INT(5) AUTO_INCREMENT, a_name VARCHAR(64) NOT NULL UNIQUE, PRIMARY KEY (a_id))",
    "CREATE TABLE category (ca_id INT(3) AUTO_INCREMENT, ca_name VARCHAR(64) NOT NULL UNIQUE, PRIMARY KEY (ca_id))",
    "CREATE TABLE course (c_id INT(5) AUTO_INCREMENT, c_name VARCHAR(64) NOT NULL UNIQUE, ca_id INT(3) NOT NULL, info VARCHAR(256), price DECIMAL(6, 2), PRIMARY KEY (c_id), FOREIGN KEY (ca_id) REFERENCES category(ca_id))",
    "CREATE TABLE course_ingredient (c_id INT(5), i_id INT(6), PRIMARY KEY (c_id, i_id), FOREIGN KEY (c_id) REFERENCES course(c_id), FOREIGN KEY (i_id) REFERENCES ingredient(i_id))",
    "CREATE TABLE selection_category (sc_id INT(3) AUTO_INCREMENT, sc_name VARCHAR(64) NOT NULL UNIQUE, PRIMARY KEY (sc_id))",
    "CREATE TABLE selection (s_id INT(6) AUTO_INCREMENT, s_name VARCHAR(64) NOT NULL UNIQUE, sc_id INT(3), i_id INT(6), s_price DECIMAL(6, 2), PRIMARY KEY (s_id), FOREIGN KEY (sc_id) REFERENCES selection_category(sc_id), FOREIGN KEY (i_id) REFERENCES ingredient(i_id))",
    "CREATE TABLE course_selection (c_id INT(5), s_id INT(6), PRIMARY KEY (c_id, s_id), FOREIGN KEY (c_id) REFERENCES course(c_id), FOREIGN KEY (s_id) REFERENCES selection(s_id))",
    "CREATE TABLE ingredient_allergene (i_id INT(6), a_id INT(5), PRIMARY KEY (i_id, a_id), FOREIGN KEY (i_id) REFERENCES ingredient(i_id), FOREIGN KEY (a_id) REFERENCES allergene(a_id))"
  ]

  for query in table_queries:
    cursor.execute(query)

  insert_queries = [
    "INSERT INTO ingredient (i_name, available) VALUES ('ingredient alpha', true), ('ingredient bravo', true), ('ingredient charlie', true), ('ingredient delta', true), ('ingredient echo', true)",
    "INSERT INTO allergene (a_name) VALUES ('allergene alpha'), ('allergene bravo'), ('allergene charlie'), ('allergene delta'), ('allergene echo')",
    "INSERT INTO category (ca_name) VALUES ('category alpha'), ('category bravo'), ('category charlie'),('category delta')",
    "INSERT INTO course (c_name, ca_id, info, price) VALUES ('course alpha', 1, 'info alpha', '5.20'), ('course bravo', 2, 'info bravo', '4.20'), ('course charlie', 1, 'info charlie', '3.75'), ('course delta', 3, 'info delta', '2.10'), ('course echo', 4, 'info echo', '7.40')",
    "INSERT INTO course_ingredient (c_id, i_id) VALUES (1, 1), (1, 3), (2, 2), (2, 5), (2, 1), (3, 1), (3, 3), (4, 5), (4, 1), (5, 1), (5, 2), (5, 3)",
    "INSERT INTO selection_category (sc_name) VALUES ('selection category alpha'), ('selection category bravo')",
    "INSERT INTO selection (s_name, sc_id, i_id, s_price) VALUES ('selection alpha', 1, NULL, NULL), ('selection bravo', 2, 2, '4.56'), ('selection charlie', 1, 1, '2.16'), ('selection delta', 1, 1, '1.26')",
    "INSERT INTO course_selection (c_id, s_id) VALUES (1, 1), (1, 2), (2, 2), (3, 3), (4, 1), (4, 2)",
    "INSERT INTO ingredient_allergene (i_id, a_id) VALUES (1, 2), (2, 3), (1, 3)"
  ]

  # Insertion requires a commit and therefore needs its own loop

  for query in insert_queries:
    cursor.execute(query)
    db.commit()
  db.close()

def drop_test_db():
  db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database=database
  )
  cursor = db.cursor()
  cursor.execute("DROP DATABASE IF EXISTS " + database)
  db.close()


# Debug only
if __name__ == '__main__':
  create_test_db()







