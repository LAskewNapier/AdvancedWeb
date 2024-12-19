#for working out HP for Creatures
import math
from ctypes.wintypes import SIZE
from email.message import Message

from flask import Flask, url_for, render_template, request, redirect, session, g
#for working out HP for Creatures and dice rolls
import random
import sqlite3, configparser, secrets, bcrypt

app = Flask(__name__)
app.secret_key = 'KAy32DSE[!dwsx@;ws6rc'
db_location = 'var/Accounts.db'

def init(app):
    config = configparser.ConfigParser()
    try:
        print("INIT FUNCTION")
        config_location = 'etc/default.cfg'
        config.read(config_location)

        app.config['DEBUG'] = config.get("config", "debug")
        app.config['ip_address'] = config.get("config", "ip_address")
        app.config['port'] = config.get("config", "port")
        app.config['url'] = config.get("config", "url")
    except:
        print("INIT ERROR AT: ", config_location)

init(app)


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = sqlite3.connect(db_location)
        g.db = db
        db.execute("PRAGMA foreign_keys = ON")
        db.commit()
    return db

@app.teardown_appcontext
def close_db(db):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('var/AccountsTables.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route("/")
def index():
    session['logged_in'] = False
    return render_template('Home.html')

@app.route("/Home")
def home():
    return render_template('Home.html')

@app.route("/about")
def about():
    return render_template('Info.html')

@app.route("/LogOut")
def LogOut():
    session.clear()
    session['logged_in'] = False
    return redirect(url_for('home'))

@app.route("/Login", methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        Username = request.form['Username']
        Password = request.form['Password']
        session['logged_in'] = False

        db = get_db()
        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        sql = """SELECT user_id, username, password FROM Users WHERE username = ?;"""

        try:
            cursor.execute(sql, (Username,))
            result = cursor.fetchone()

            if result:
                if bcrypt.checkpw(Password.encode('utf-8'), result['password']):
                    session['id'] = result['user_id']
                    session['username'] = result['username']
                    session['logged_in'] = True
                    username = session['username']
                    return redirect(url_for('Profile', username=username))
            else:
                session['logged_in'] = False
                error = 'no data reseved'
                return render_template('Login.html', Message=error)



        except:
            error = 'Invalid username or password'
            return render_template('Login.html', Message=error)
    else:
        return render_template('Login.html')

@app.route("/SignUp", methods=['GET', 'POST'])
def SignUp():
    if request.method == 'POST':
        email = request.form['Email']
        username = request.form['Username']
        password = request.form['Password']
        repassword = request.form['rePassword']

        if password == repassword:
            passcrypt = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            db = get_db()
            db.row_factory = sqlite3.Row
            cursor = db.cursor()

            CheckQuery = """SELECT email, username FROM Users WHERE username = ? or email = ?;"""

            try:
                cursor.execute(CheckQuery, (username, email))
                result = cursor.fetchone()

                if result:
                    if result['username'] == username and result['email'] == email:
                        error = 'Email And username already in use, try Logging in'
                        return render_template('SignUp.html', Message=error)
                    elif result['username'] == username:
                        error = 'Username already in use, try Logging in'
                        return render_template('SignUp.html', Message=error)
                    elif result['email'] == email:
                        error = 'Email already in use, try Logging in'
                        return render_template('SignUp.html', Message=error)

                insert_query = """INSERT INTO Users (username, email, password) VALUES (?, ?, ?);"""
                cursor.execute(insert_query, (username, email, passcrypt))
                db.commit()
                message = 'User {} successfully created!'.format(username)
                return redirect(url_for('Login', Message=message))
            except:
                return render_template('SignUp.html', Message="An error occurred, Please try again")
        else:
            error = 'passwords do not match'
            return render_template('SignUp.html', Message=error)
    else:
        return render_template('SignUp.html')

@app.route("/Profile/<username>")
def Profile(username):
    username = username

    db = get_db()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    UsersCreations = """SELECT Creature_id, cName FROM Creatures WHERE user_id = ?;"""

    id=session['id']

    try:
        cursor.execute(UsersCreations, (id,))
        result = cursor.fetchone()
        name = result['cName']
        return render_template('Profile.html', username=username, name=name)
    except:
        name = 'error'
        return render_template('Profile.html', username=username, name=id)




@app.route("/Roller", methods=['GET', 'POST'])
def Roller():
    if request.method == 'POST':
        sides = request.form['sides']
        roll = random.randint(1, int(sides))
        returnMessage = str(roll)
        return render_template('Roller.html', rmessage=returnMessage, sides=sides)
    else:
        return render_template('Roller.html')

@app.route("/CreateCreature", methods=['GET', 'POST'])
def CreateCreature(x=1):
    if request.method == 'POST':
        HP = ""
        rHP = 0
        cName = request.form['Name']
        Type = request.form['Type']
        STR = request.form['STR']
        DEX = request.form['DEX']
        CON = request.form['CON']
        INT = request.form['INT']
        WIS = request.form['WIS']
        CHA = request.form['CHA']
        PB = request.form['PB']
        Throw = request.form['Throws']
        Size = request.form['Size']
        HDICE = request.form['HitD']
        AC = request.form['AC']

        if AC == '':
            rAC = 10 + ((int(DEX) - 10) / 2)
            AC = str(rAC)

        if Size == "Tiny":
            SizeHit = 4
        elif Size == "Small":
           SizeHit = 6
        elif Size == "Medium":
           SizeHit = 8
        elif Size == "Large":
           SizeHit = 10
        elif Size == "Huge":
           SizeHit = 12
        else:
           SizeHit = 20
        while x <= int(HDICE):
            rand = random.randint(1, SizeHit)
            rHP = rHP + rand + math.floor((int(CON) - 10) / 2)
            if rHP < 1:
                rHP = 1
            x += 1
        HP = str(rHP)
        session['S-HP'] = HP
        session['S-Name'] = cName
        session['S-AC'] = AC
        session['S-Type'] = Type
        session['S-STR'] = STR
        session['S-DEX'] = DEX
        session['S-CON'] = CON
        session['S-INT'] = INT
        session['S-WIS'] = WIS
        session['S-CHA'] = CHA
        session['S-PB'] = PB
        session['S-Throws'] = Throw
        session['S-Size'] = Size
        session['S-HitD'] = HDICE


        if session['logged_in'] == True:
            user_id = session['id']

            db = get_db()
            db.row_factory = sqlite3.Row
            cursor = db.cursor()



            insert_Creature = """INSERT INTO Creatures (cName, HP, type, STR, DEX, CON, cINT, WIS, CHA, PB, AC, THROW, SIZE, HDICE) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
            get_id = """SELECT Creature_id FROM Creatures WHERE cName = ?;"""
            try:




                print('ok')
                cursor.execute(insert_Creature, (cName, HP, Type, STR, DEX, CON, INT, WIS, CHA, PB, AC, Throw, Size, HDICE))
                print('ok')
                db.commit()
                print('ok')
                cursor.execute(get_id, (cName, ))
                print('ok')
                result = cursor.fetchone()
                print('ok')
                creature_id = result['Creature_id']
                print('ok')
                print(creature_id)
                print(user_id)
                cursor.execute(LinkTables1)
                print('ok')
                if session['creature_id'] != None:

                    cursor.execute(LinkTables, (user_id, creature_id))
                    print('ok')

                message = 'You have successfully made a creature with this name'
                return redirect(url_for('Display', Name=cName))



            except:
                return render_template('CreateCreature.html', Message='an error occurred')


        return redirect(url_for('Display', Name=cName))
    else:
        return render_template('CreateCreature.html')

@app.route("/Display//<Name>")
def Display(Name=None):
    HP = session['S-HP']
    AC = session['S-AC']
    Type = session['S-Type']
    STR = session['S-STR']
    DEX = session['S-DEX']
    CON = session['S-CON']
    INT = session['S-INT']
    WIS = session['S-WIS']
    CHA = session['S-CHA']
    PB = session['S-PB']
    Throws = session['S-Throws']
    Size = session['S-Size']
    HitD = session['S-HitD']

    return render_template('Display.html', Name=Name, Health=HP, AC=AC, Type=Type, STR=STR, DEX=DEX, CON=CON, INT=INT, WIS=WIS, CHA=CHA, PB=PB, Throws=Throws, Size=Size, HitD=HitD)

if __name__ == '__main__':
    init(app)
    app.run(host=app.config['ip_address'], debug=True, port=int(app.config['port']))