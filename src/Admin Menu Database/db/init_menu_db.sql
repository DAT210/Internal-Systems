DROP DATABASE IF EXISTS menu;

CREATE DATABASE menu;

USE menu;

CREATE TABLE ingredient (
	i_id INT(6) AUTO_INCREMENT,
    i_name VARCHAR(64) NOT NULL UNIQUE,
    available BOOLEAN,
    PRIMARY KEY (i_id)
);


CREATE TABLE allergene (
	a_id INT(5) AUTO_INCREMENT,
    a_name VARCHAR(64) NOT NULL UNIQUE,
    PRIMARY KEY (a_id)
);

CREATE TABLE category (
	ca_id INT(3) AUTO_INCREMENT,
    ca_name VARCHAR(64) NOT NULL UNIQUE,
    PRIMARY KEY (ca_id)
);


CREATE TABLE course (
	c_id INT(5) AUTO_INCREMENT,
    c_name VARCHAR(64) NOT NULL UNIQUE,
    ca_id INT(3) NOT NULL,
    info VARCHAR(256),
    price DECIMAL(6, 2),
    PRIMARY KEY (c_id),
    FOREIGN KEY (ca_id) REFERENCES category(ca_id)
);


CREATE TABLE course_ingredient (
	c_id INT(5),
    i_id INT(6),
    PRIMARY KEY (c_id, i_id),
    FOREIGN KEY (c_id) REFERENCES course(c_id),
	FOREIGN KEY (i_id) REFERENCES ingredient(i_id)
);


CREATE TABLE selection_category (
	sc_id INT(3) AUTO_INCREMENT,
    sc_name VARCHAR(64) NOT NULL UNIQUE,
    PRIMARY KEY (sc_id)
);


CREATE TABLE selection (
	s_id INT(6) AUTO_INCREMENT,
    s_name VARCHAR(64) NOT NULL UNIQUE,
    sc_id INT(3),
    i_id INT(6),
    s_price DECIMAL(6, 2),
    PRIMARY KEY (s_id),
    FOREIGN KEY (sc_id) REFERENCES selection_category(sc_id),
    FOREIGN KEY (i_id) REFERENCES ingredient(i_id)
);


CREATE TABLE course_selection (
	c_id INT(5),
    s_id INT(6),
    PRIMARY KEY (c_id, s_id),
    FOREIGN KEY (c_id) REFERENCES course(c_id),
    FOREIGN KEY (s_id) REFERENCES selection(s_id)
);


CREATE TABLE ingredient_allergene (
	i_id INT(6),
	a_id INT(5),
    PRIMARY KEY (i_id, a_id),
    FOREIGN KEY (i_id) REFERENCES ingredient(i_id),
    FOREIGN KEY (a_id) REFERENCES allergene(a_id)
);

/* Add values to the database */

INSERT INTO ingredient (i_name, available) VALUES
	("Pine Nuts", true),
    ("Pineapple", true),
    ("Wheat Flour", true),
    ("Eggs", true),
    ("Onion Rings", true),
    ("Caesar Salad", true),
    ("Lemon", true),
    ("Asparagus", true),
    ("Bacon", true),
    ("Butter", true),
    ("Serrano Ham", true),
    ("Halloumi", true),
    ("Tequila", true),
    ("Orange Juice", true),
    ("Grenadine", true),
    ("Vodka", true),
    ("Tomato Juice", true),
    ("Tabasco Sauce", true),
    ("Mint Leaves", true),
    ("Gin", true),
    ("Ginger beer", true),
    ("Strawberries", true),
    ("Sprite", true),
    ("Club Soda", true),
    ("Lime", true),
    ("Chicken Breast", true),
    ("Peanut Sauce", true),
    ("Jalapeño", true),
    ("Lobster", true),
    ("Bread", true),
    ("Garlic", true),
    ("Steak", true),
    ("Red Onions", true),
    ("Potatoes", true),
    ("Red Wine Sauce", true),
    ("Carrots", true),
    ("Tomatoes", true),
    ("Pasta", true),
    ("Potato Fries", true),
    ("Ground beef", true),
    ("Lasagna Noodles", true),
    ("Parmesan Cheese", true),
    ("Sugar", true),
    ("Cocoa", true),
    ("Cow Milk", true),
    ("Blueberry", true),
    ("Cream", true),
    ("Orange Liqueur", true),
    
    
    

    ("ingredient delta", true),
    ("ingredient echo", true);
    
    
INSERT INTO allergene (a_name) VALUES
	("allergene alpha"),
    ("allergene bravo"),
    ("allergene charlie"),
    ("allergene delta"),
    ("allergene echo");
    
INSERT INTO category (ca_name) VALUES 
	("Starters"),
    ("Drinks"),
    ("Main"),
    ("Dessert"),
    ("Lunch"),
    ("Dinner");
    
    
INSERT INTO course (c_name, ca_id, info, price) VALUES 
	("Pine nut sbrisalona", 1, "Sed fermentum eros vitae eros", "29.79"),
    ("Aenean eu", 1, "Feugiat maximus neque pharetra", "19.35"),
    ("Sed feugiat", 1, "Proin lacinia nisl ut ultricies posuere nulla", "12.19"),
    ("Consectetur", 1, "Etiam cursus facilisis tortor", "21.89"),
    ("Vivamus pretium", 2, "Sed fermentum eros vitae eros", "29.19"),
    ("Duis pharetra ligula", 2, "Feugiat maximus neque pharetra", "19.35"),
    ("In eu dolor", 2, "Proin lacinia nisl ut ultricies posuere nulla", "53.34"),
    ("Feugiat maximus", 2, "Sed fermentum eros vitae eros", "62.45"),
    ("Duis sed aliquet", 3, "Proin lacinia nisl ut ultricies posuere nulla", "31.18"),
    ("Suspendisse", 3, "Feugiat maximus neque pharetra", "70.25"),
    ("Scelerisque sed", 3, "Etiam cursus facilisis tortor", "36.19"),
    ("Mollis nulla", 3, "Proin lacinia nisl ut ultricies posuere nulla", "19.50"),
    ("Convallis augue", 3, "Sed fermentum eros vitae eros", "29.15"),
    ("Maecenas tristique", 3, "Feugiat maximus neque pharetra", "29.79"),
    ("Duis tincidunt", 3, "Proin lacinia nisl ut ultricies posuere nulla", "19.35"),
    ("Tempus aliquat", 4, "Proin lacinia nisl ut ultricies posuere nulla", "9.79"),
    ("Scelerisque", 4, "Sed fermentum eros vitae eros", "19.35"),
    ("Cras maximus", 4, "Duis pharetra ligula at urna dignissim", "5.79"),
    ("Sed varius", 5, "Aenean pharetra tortor dui in pellentesque", "29.79"),
    ("Sbrisalona", 5, "Proin lacinia nisl ut ultricies posuere nulla", "29.79"),
    ("Tempus aliquet", 5, "Aenean condimentum ante era", "45.09"),
    ("Cras eget magna", 5, "Sed fermentum eros vitae eros", "45.09"),
    ("Duis massa", 5, "Proin lacinia nisl ut ultricies posuere nulla", "12.75"),
    ("Nullam maximus", 5, "Duis massa nibh porttitor nec imperdiet eget", "12.75"),
    ("Maecenes tristique", 6, "Aenean pharetra tortor dui in pellentesque", "29.79"),
    ("Chras maximus", 6, "Proin lacinia nisl ut ultricies posuere nulla", "29.79"),
    ("Pine nut sbrisalone", 6, "Aenean condimentum ante erat", "45.09"),
    ("Pine not sbrisalona", 6, "Sed fermentum eros vitae eros", "45.09"),
    ("Suspendisse eu", 6, "Proin lacinia nisl ut ultricies posuere nulla", "12.75"),
    ("Tempor malesuada", 6, "Duis massa nibh porttitor nec imperdiet eget", "12.75");
  
    
INSERT INTO course_ingredient (c_id, i_id) VALUES
	/* Starters */
	(1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 5),
    (2, 6),
    (2, 7),
    (3, 8),
    (3, 9),
    (3, 10),
    /* Drinks */
    (4, 11),
    (4, 12),
    (4, 6),
    (5, 13),
    (5, 14),
    (5, 15),
    (6, 16),
    (6, 17),
    (6, 18),
    (6, 7),
    (7, 19),
    (7, 20),
    (7, 21),
    (8, 16),
    (8, 22),
    (8, 23),
    (8, 24),
    (8, 25),
    /* Mains */
    (9, 26),
    (9, 27),
    (9, 28),
    (10, 29),
    (10, 30),
    (10, 31),
    (10, 7),
    (11, 32),
    (11, 33),
    (11, 34),
    (11, 35),
    (12, 34),
    (12, 36),
    (12, 37),
    (13, 38),
    (13, 37),
    (13, 26),
    (14, 32),
    (14, 39),
    (14, 26),
    (15, 40),
    (15, 41),
    (15, 26),
    (15, 42),
    /* Desserts */
    (16, 43),
    (16, 44),
    (16, 45),
    (16, 3),
    (16, 10),
    (17, 46),
    (17, 3),
    (17, 4),
    (17, 10),
    (18, 47),
    (18, 43),
    (18, 4),
    (18, 48),
    
    
    

    
    (4, 5),
    (4, 1),
    (5, 1),
    (5, 2),
    (5, 3);
    
    
INSERT INTO selection_category (sc_name) VALUES 
	("selection category alpha"),
    ("selection category bravo");
    
    
INSERT INTO selection (s_name, sc_id, i_id, s_price) VALUES 
	("selection alpha", 1, NULL, NULL),
    ("selection bravo", 2, 2, "1.29"),
    ("selection charlie", 1, 1, "0.67"),
    ("selection delta", 1, 1, "10.65");
    
    
INSERT INTO course_selection (c_id, s_id) VALUES 
	(1, 1),
    (1, 2),
    (2, 2),
    (3, 3),
    (4, 1),
    (4, 2);
  
  
INSERT INTO ingredient_allergene (i_id, a_id) VALUES
	(1, 2),
    (2, 3),
    (1, 3);