from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def HeadPage():
    return render_template("header.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
