import urllib.request
import json
import math
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt

# Consts
access_token = '5c1b71db5c1b71db5c1b71db135c79faf355c1b5c1b71db06c6a4e7e845f049096d2eef'
max_count = 100


def count_words(string):
    return 1 + string.count(' ')


def get_user_info(user_id):
    user = {}
    url = urllib.request.Request('https://api.vk.com/method/users.get?v=5.74' +
                                 '&name_case=Nom' +
                                 '&access_token=' + access_token +
                                 '&user_id=' + str(user_id) +
                                 '&fields=bdate,city')
    response = json.loads(
        urllib.request.urlopen(url).read().decode('utf-8')
    )

    if response.get('response'):
        if response['response'][0].get('bdate'):
            if len(response['response'][0]['bdate']) > 5:
                bdate = datetime.strptime(response['response'][0]['bdate'], '%d.%m.%Y')
                today = datetime.today()
                user['age'] = today.year - bdate.year
                if (bdate.month > today.month) | (bdate.month == today.month & bdate.day > today.day):
                    user['age'] -= 1
        if response['response'][0].get('city'):
            user['city'] = response['response'][0]['city']['title']
    else:
        if response.get('error'):
            print('Get user error: ' + response['error']['error_msg'])

    return user


def get_comments(owner_id, post_id, comments_count):
    result = []
    for number in range(int(math.ceil(comments_count / max_count))):
        offset = number * 100
        count = min(comments_count - offset, 100)

        url = urllib.request.Request('https://api.vk.com/method/wall.getComments?v=5.74' +
                                     '&access_token=' + access_token +
                                     '&owner_id=' + str(owner_id) +
                                     '&post_id=' + str(post_id) +
                                     '&offset=' + str(offset) +
                                     '&count=' + str(count))
        response = json.loads(
            urllib.request.urlopen(url).read().decode('utf-8')
        )

        if response.get('response'):
            items = response['response']['items']
            for i in range(len(items)):
                comment = {
                    'text': items[i]['text'],
                    'length': count_words(items[i]['text']),
                }
                if items[i]['from_id'] > 0:
                    comment['user'] = get_user_info(items[i]['from_id'])
                result.append(comment)
        else:
            if response.get('error'):
                print('Get comments error: ' + response['error']['error_msg'])

    return result


def get_posts(owner_id, posts_count, comments_count):
    result = []
    for number in range(int(math.ceil(posts_count / max_count))):
        offset = number * 100
        count = min(posts_count - offset, 100)

        url = urllib.request.Request('https://api.vk.com/method/wall.get?v=5.74' +
                                     '&access_token=' + access_token +
                                     '&owner_id=' + str(owner_id) +
                                     '&offset=' + str(offset) +
                                     '&count=' + str(count))
        response = json.loads(
            urllib.request.urlopen(url).read().decode('utf-8')
        )

        if response.get('response'):
            items = response['response']['items']
            for i in range(len(items)):
                # Log process
                print(str(offset + i + 1) + ' / ' + str(min(posts_count, response['response']['count'])) + ' posts')
                # Get post data
                post = {
                    'text': items[i]['text'],
                    'length': count_words(items[i]['text']),
                    'comments': get_comments(owner_id, items[i]['id'], comments_count),
                }
                if items[i]['from_id'] > 0:
                    post['user'] = get_user_info(items[i]['from_id'])

                result.append(post)
        else:
            if response.get('error'):
                print('Get posts error: ' + response['error']['error_msg'])

    return result


# Parameters
owner_id = -1
posts_count = 10
comments_count = 5

# Get posts
posts = get_posts(owner_id, posts_count, comments_count)

f, (lengths, posts_ages, comments_ages, posts_cities, comments_cities) = plt.subplots(1, 5)

for post in posts:
    if len(post['comments']) > 0:
        average = 0
        for comment in post['comments']:
            average += comment['length']
        average /= len(post['comments'])
        lengths.scatter(post['length'], average)
lengths.set_xlabel('Длина поста')
lengths.set_ylabel('Длина комментария')

for post in posts:
    ages = []
    if post.get('user'):
        if post['user'].get('age'):
            ages.append([post['user']['age'], post['length']])

    for age in ages:
        posts_ages.scatter(age[0], age[1])
posts_ages.set_xlabel('Возраст')
posts_ages.set_ylabel('Длина поста')

for post in posts:
    ages = []
    for comment in post['comments']:
        if comment.get('user'):
            if comment['user'].get('age'):
                ages.append([comment['user']['age'], comment['length']])

    for age in ages:
        comments_ages.scatter(age[0], age[1])
comments_ages.set_xlabel('Возраст')
comments_ages.set_ylabel('Длина комментария')

for post in posts:
    ages = []
    if post.get('user'):
        if post['user'].get('city'):
            ages.append([post['user']['city'], post['length']])

    for age in ages:
        posts_cities.scatter(age[0], age[1])
posts_cities.set_xlabel('Город')
posts_cities.set_ylabel('Длина поста')

for post in posts:
    ages = []
    for comment in post['comments']:
        if comment.get('user'):
            if comment['user'].get('city'):
                ages.append([comment['user']['city'], comment['length']])

    for age in ages:
        comments_cities.scatter(age[0], age[1])
comments_cities.set_xlabel('Город')
comments_cities.set_ylabel('Длина комментария')

plt.show()

# Save in file
with open('result.json', 'w') as file:
    file.write(json.dumps(posts))
    file.close()
