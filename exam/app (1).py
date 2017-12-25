from flask import Markup
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__, template_folder="views")

import json

eng_to_thai = json.loads(open('./english_to_thai.json').read())

@app.route("/")
def main_page():
    eng = request.args.get('word')
    thai = "Не найдено"

    if eng != None:
        if eng in eng_to_thai.keys():
            thai = eng_to_thai[eng]

    return render_template("index.html", eng=eng, thai=thai) 

def main():
    app.run(host='0.0.0.0')

if __name__ == "__main__":
    main()
