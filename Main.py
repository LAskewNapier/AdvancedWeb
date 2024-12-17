from flask import Flask, url_for, render_template, request, redirect
import random

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)