from flask import Markup
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__, template_folder="views")

@app.route("/")
def main_page():
    eng = request.args.get('word')
    return render_template("index.html", eng=eng, thai="tr") 

def main():
    app.run(host='0.0.0.0')

if __name__ == "__main__":
    main()

