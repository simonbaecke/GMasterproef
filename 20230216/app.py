from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/test', methods=['POST'])
def test():
    zipcode = request.form['zip']
    return render_template('test.html', temp=zipcode)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)