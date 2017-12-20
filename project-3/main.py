# -*- coding: utf-8 -*-
from importlib import reload

from flask import Markup
import urllib.request
from flask import Flask
from flask import render_template
from flask import request
from todorev import translateString
from bs4 import BeautifulSoup
from pogoda import getPogodaHTML
from quiz import Quiz

app = Flask(__name__, template_folder="views")

@app.route("/")
def main_page():

    rus = request.args.get('word')
    slov = translateString(rus) if rus else None

    return render_template("index.html", vars={"rus":rus, "slov":slov}, pogoda=Markup(getPogodaHTML())) 

@app.route("/test")
def test_page():
    user_answers = {}
    for i in range(10):
        asw_name = 'quiz' + str(i)
        asw_value = request.args.get(asw_name)
        if asw_value:
            user_answers[i] = asw_value


    return render_template("test.html", quiz=Quiz, user_answers=user_answers) 


@app.route("/lenta")
def lentaRu_page():
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0"}
    
    res = urllib.request.urlopen("http://lenta.ru/")
    soup = BeautifulSoup(res, "html.parser")

    def changeText(DOM):
        for tag in DOM:
            try:
                tag.string.replace_with(translateString(tag.string))
            except AttributeError:
                if hasattr(tag, 'children'):
                    for child in tag.children:
                        changeText(child)

    changeText(soup.findAll())
    return str(soup)
