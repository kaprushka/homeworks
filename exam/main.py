import os
import json
from bs4 import BeautifulSoup


def getHtml(file_name):
    return open(file_name).read()

def getTable(tdict, html):

    parsed = BeautifulSoup(html, "html.parser")
    try:
        table = parsed.find('table', class_="gridtable")
        thai_words = table.select('a[href^="/id/"]')
        for tw in thai_words:
            try:
                tdict[tw.getText()] = tw.parent.parent('td')[-1].getText()
            except IndexError:
                pass
    except:
        pass

def tr_all_htlm_if_folder(folder, my_dict):
    pages = os.listdir(folder)
    for page in pages:
        getTable(my_dict, getHtml(folder + page))

if __name__ == "__main__":
    thai_dict = {}
    tr_all_htlm_if_folder('./thai_pages/', thai_dict)

    with open('thai_dict.json', 'w') as outfile:
        json.dump(thai_dict, outfile)

    english_to_thai = {v: k for k, v in thai_dict.items()}

    with open('english_to_thai.json', 'w') as outfile:
        json.dump(english_to_thai, outfile)