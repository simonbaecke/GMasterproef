from flask import Flask, render_template,redirect,url_for

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def home():
    antwoord = 5+5
    return render_template("home.html",antwoord=antwoord)

if __name__ == "__main__":
    app.run(debug=True)