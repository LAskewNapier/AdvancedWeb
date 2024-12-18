#for working out HP for Creatures
import math

from flask import Flask, url_for, render_template, request, redirect, session
#for working out HP for Creatures and dice rolls
import random

app = Flask(__name__)
app.secret_key = 'KAy32DSE[!dwsx@;ws6rc'
@app.route("/")
def index():
    return render_template('Home.html')

@app.route("/Home")
def home():
    return render_template('Home.html')

@app.route("/about")
def about():
    return render_template('Info.html')

@app.route("/Login")
def Login():
    return render_template('Login.html')

@app.route("/SignUp")
def SignUp():
    return render_template('SignUp.html')

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
        HP = 0
        Name = request.form['Name']
        Type = request.form['Type']
        STR = request.form['STR']
        DEX = request.form['DEX']
        CON = request.form['CON']
        INT = request.form['INT']
        WIS = request.form['WIS']
        CHA = request.form['CHA']
        PB = request.form['PB']
        Throws = request.form['Throws']
        Size = request.form['Size']
        HitD = request.form['HitD']

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
        while x <= int(HitD):
            rand = random.randint(1, SizeHit)
            HP = HP + rand + ((int(CON) - 10) / 2)
            if HP < 1:
                HP = 1
            x += 1
        HP = math.floor(HP)
        session['S-HP'] = HP
        session['S-Name'] = Name
        session['S-Type'] = Type
        session['S-STR'] = STR
        session['S-DEX'] = DEX
        session['S-CON'] = CON
        session['S-INT'] = INT
        session['S-WIS'] = WIS
        session['S-CHA'] = CHA
        session['S-PB'] = PB
        session['S-Throws'] = Throws
        session['S-Size'] = Size
        session['S-HitD'] = HitD
        return redirect(url_for('Display', Name=Name))
    else:
        return render_template('CreateCreature.html')
@app.route("/Display/<Name>")
def Display(Name):
    HP = session['S-HP']
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
    return render_template('Display.html', Name=Name, Health=HP, Type=Type, STR=STR, DEX=DEX, CON=CON, INT=INT, WIS=WIS, CHA=CHA, PB=PB, Throws=Throws, Size=Size, HitD=HitD)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)