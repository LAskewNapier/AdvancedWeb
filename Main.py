from flask import Flask, url_for, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Home.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)