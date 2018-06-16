# -*- coding: utf-8 -*-

import re
import time
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup


def transform_date(date_string):
    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')


source_url = 'https://iz.ru/'
source_url_kultura = 'https://iz.ru/rubric/kultura'

content = requests.get(source_url_kultura)
soup = BeautifulSoup(content.text, 'html.parser')

stories = soup.findAll('div', {'class': 'two-infographic-block__item__inside__info__description description-box '})
urls = soup.findAll('a')
regex = re.compile("\/\d+\/([a-z-]+|[\d-]+)\/(.?)*")

url_stories = []
for url in urls:
    if 'href' in url.attrs.keys() and re.match(regex, url.attrs['href']):
        url_stories.append(url.attrs['href'])

articles = []

N = 50
url_stories_short = url_stories[:N]
for i, url in enumerate(url_stories_short[len(articles):]):
    print('Progress:', i)
    current_url = source_url[:-1] + url
    content = requests.get(current_url)
    soup = BeautifulSoup(content.text, 'html.parser')
    current_text = []
    article_body = soup.findAll('div', {'itemprop': 'articleBody'})
    if len(article_body) > 0:
        for paragraph in article_body[0].findAll(['p', re.compile('^h[1-6]$')]):
            if len(paragraph.text.strip()) > 0:
                current_text.append(paragraph.text.replace('\xa0', ' '))
        current_text = ' '.join(current_text)
        current_date = soup.find('time').attrs['datetime']
        articles.append({'text': current_text, 'url': current_url, 'date': current_date})
    time.sleep(3)

current_data = pd.DataFrame(articles)
current_data.drop_duplicates(subset='text', inplace=True)

old_data = pd.read_csv('iz.csv')

current_data['timestamp'] = current_data['date'].apply(transform_date)
current_data['time_difference'] = [x.days for x in datetime.now() - current_data['timestamp']]
all_data = pd.concat([old_data, current_data])
all_data.drop_duplicates(subset='text', inplace=True)
all_data.to_csv('iz.csv', index=False)
