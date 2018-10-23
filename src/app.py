
from flask import Flask,render_template,g, request,session,redirect,url_for
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash #could not install npm package to the dependencies, hence its not in the package.json
import datetime

app = Flask(__name__)
app.debug = True
app.secret_key = "153felgdgorjdr123,fesgsb/?+fef" #if you know a better implementation for creating secure secret keys change this. NB! Random generated are secret keys are not recommended by the interwebs.
app.config.password = "MySQLNetty6"
app.config.dbinfo = {
    "user": "root",
    "password": app.config.password,
    "host": "localhost",
    "database": "dat210_admin"
}

salt = "53trig43ddf"

#database get queries
app.config.getqueries = {
    "getallusers": "SELECT * FROM user"
}
#getallusers = "SELECT * FROM user"

#Sets up the database connection
def get_db():
    if not hasattr(g,"_database"):
        #change depending on user
        g._database = mysql.connector.connect(user= app.config.dbinfo["user"], password = app.config.dbinfo["password"], host = app.config.dbinfo["host"], database = app.config.dbinfo["database"])
        #g._database = mysql.connector.connect(user="root", password="MySQLNetty6", host="localhost", database="dat210_admin")

    return g._database

@app.teardown_appcontext
def teardown_db(error):
    """ Closes the database at the end of the request."""
    db = getattr(g, "_database",None)
    if db is not None:
        db.close()

#none route methods
def checkpassword(checkbox,username,password):
    #checks if the password given matches with any of the passwords matching the given username
    verified = False
    truepassword = password+salt
    for user in checkbox.keys():
        if user == username:
            print(checkbox)
            if check_password_hash(checkbox[username]["pass"],truepassword):
                verified = True
                break

    return verified

def checkusercriteria(username,password):
    #check if given username and password are allowed to be stored.
    if len(username) < 5 or len(password) < 5:
        return False
    return True


#route methods
@app.route("/")
def index():
    if "username" not in session:
        return render_template("restrictions/login.html")

    return render_template("index.html",user = session["username"],auth=session["authority"])

@app.route("/logoff")
def logoff():
    if "username" not in session:
        return redirect(url_for("index"))
    else:
        session.pop("username")
        session.pop("authority")
        return render_template("restrictions/login.html", logoff="You successfully signed out")

@app.route("/GCU",methods=["GET"])
def GCU():
    if "username" not in session:
        return redirect(url_for("index"))
    elif session["authority"] > 1:
        return render_template("restrictions/accessdenied.html")
    else:
        return render_template("restrictions/CreateUsers.html", user =session["username"])

@app.route("/login",methods=["POST"])
def login():
    confirmed = False

    username = request.form.get("username")
    password = request.form.get("password")
    #print("username: {}".format(username))
    #print("password: {}".format(password))

    conn = get_db()
    cursor = conn.cursor()
    userdict = {}
    try:
        cursor.execute(app.config.getqueries["getallusers"])
        for user, passw, authority in cursor:
            userdict[user] = {"pass": passw, "auth": authority}
    except mysql.connector.Error as err:
        print("Error {}".format(err.msg))
    finally:
        conn.close()

    confirmed = checkpassword(userdict,username,password)
    print(confirmed)
    if confirmed is True:
        session["username"] = username
        session["authority"] = userdict[username]["auth"]
        #print(session)
        return render_template("index.html",user = session["username"],auth = session["authority"])

    return render_template("restrictions/login.html", failure=True, username=username, password=password)

@app.route("/CreateUser",methods=["POST"])
def CreateUser():
    username = request.form.get("username")
    #print(username)
    password = request.form.get("passw")
    #print(password)
    authlvl = request.form.get("SelectAuthlvl")
    print(authlvl)

    success = True
    if checkusercriteria(username,password) is False:
        success = False

    else:
        passalt = password + salt
        hashedpass = generate_password_hash(passalt)
        conn = get_db()
        cursor = conn.cursor()
        try:
            statement = ("INSERT INTO user(username,password,authority_level) VALUES('{username}','{passw}',{authority})".format(username=username,passw=hashedpass,authority=authlvl))
            cursor.execute(statement)
            conn.commit()
        except mysql.connector.Error as err:
            print("Error {}".format(err.msg))
            success = False
        finally:
            cursor.close()

    if success is True:
        print("successful")
        return render_template("restrictions/CreateUsers.html", success=success)
    else:
        print("failure")
        return render_template("restrictions/CreateUsers.html", username=username, passw=password, success=success)

#timesheet related

@app.route("/timesheet")
def timesheet():
    if "username" not in session:
        return redirect(url_for("index"))
    return render_template("calendar.html")


@app.route("/timesheet/<string:work_date>")
def workers(work_date):
    if "username" not in session:
        return redirect(url_for("index"))

    date_splitted = work_date.split("-")
    final_date = date_splitted[2] + "-" + date_splitted[1] + "-" + date_splitted[0]
    entries = []
    db = get_db()
    cur = db.cursor(buffered=True)
    try:
        sql = "SELECT * FROM Timesheet WHERE work_date=%s"
        cur.execute(sql, (final_date,))

        for _ in range(0, cur.rowcount):
            row = cur.fetchone()
            entries.append({
                "employee_id": row[0],
                "work_date": row[1],
                "work_start": row[2],
                "work_finish": row[3],
                "clock_in": row[4],
                "clock_out": row[5],
            })
    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
    finally:
        cur.close()

    return render_template("work_date.html", workers=entries, date=work_date)

@app.route("/canceltimesheet",methods=["POST"])
def canceltimesheet():
    ""

@app.route("/timesheet/<string:work_date>/<int:employee_id>")
def form_check(work_date, employee_id):
    timestamp = str(datetime.datetime.now().time())
    time_splitted = timestamp.split(".")
    time = time_splitted[0]
    return render_template("form_check.html", employee_id=employee_id, date=work_date, time=time)


@app.route("/timesheet/validate", methods=["POST"])
def validate():
    employee_id = request.form.get("employee")
    date = request.form.get("date")
    time = request.form.get("timestamp")

    employee_id = int(employee_id)

    print("Date from form: " + date)

    '''Format for the date object in the database is the inverted from the javascript/web application DB: YYYY-MM-DD, JS: DD-MM-YYYY'''
    date_splitted = date.split("-")
    final_date = date_splitted[2] + "-" + date_splitted[1] + "-" + date_splitted[0]

    print("Date rearranged for db: " + final_date)

    db = get_db()
    cur = db.cursor(buffered=True)
    try:
        sql = "SELECT * FROM Timesheet WHERE employee_id=%s AND work_date=%s"
        cur.execute(sql, (employee_id, final_date,))

        row = cur.fetchone()
        if row[4] == None:
            sql = "UPDATE Timesheet SET clock_in=%s WHERE employee_id=%s AND work_date=%s"
        else:
            sql = "UPDATE Timesheet SET clock_out=%s WHERE employee_id=%s AND work_date=%s"

        cur.execute(sql, (time, employee_id, final_date,))
        db.commit()

    except mysql.connector.Error as err:
        print("Error: {}".format(err.msg))
    finally:
        cur.close()

    return redirect(url_for('workers', work_date=date))

if __name__ == "__main__":
    app.run()

