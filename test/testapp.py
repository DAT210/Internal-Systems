
from src.app import checkpassword,checkusercriteria
import mysql.connector


def test_checkusernamepassword():
    username = "admin"
    password = "admin123"
    checkbox = {}
    dbtest = True

    dbpassword = "INSERT PASSWORD HERE!" #Use your own db password
    conn = mysql.connector.connect(user='root', password=dbpassword, host='localhost', database='dat210_admin')
    cursor = conn.cursor()

    query = "SELECT * FROM user"
    try:
        cursor.execute(query)
        for user, passw, authority in cursor:
            checkbox[user] = {"pass": passw, "auth": authority}
    except mysql.connector.Error as err:
        print("Error {}".format(err.msg))
        dbtest = False
    finally:
        conn.close()

    if dbtest is True:
        test = checkpassword(checkbox,username,password)
    else:
        test = False
    assert test == True

def test_checkusercriteriaver1():
    username = "test2"
    password = "12342"
    test = checkusercriteria(username,password)
    assert test == True
