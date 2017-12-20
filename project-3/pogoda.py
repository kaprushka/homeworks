from bs4 import BeautifulSoup
import urllib.request

def getPogodaHTML():

    pogoda_html = "<h5>Погода не загрузилать</h5>"
    pogoda_url = "https://yandex.ru/pogoda/skopje"
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0"}
    
    try:
        res = urllib.request.urlopen(pogoda_url)
        soup = BeautifulSoup(res, "html.parser")
        pogoda_html = soup.find(class_='fact')
        for a in pogoda_html.findAll('a'):
            a['href'] = pogoda_url
    except:
        pass

    return str(pogoda_html)