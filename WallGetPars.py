import csv

import requests
from config import VK_API_TOKEN


def get_wall_posts(domain):
    wall_get_method = 'https://api.vk.com/method/wall.get'
    version = 5.103
    count = 10

    params = {
        'access_token': VK_API_TOKEN,
        'v': version,
        'domain': domain,
        'count': count,
    }

    all_posts = []

    for offset in range(0, 1000, 100):
        params['offset'] = offset
        response = requests.get(wall_get_method, params=params)
        data = response.json()['response']['items']
        all_posts.extend(data)

    return all_posts


def file_writer(data):
    with open('result.csv', 'w') as file:
        pen = csv.writer(file)
        pen.writerow(('likes', 'body', 'url'))
        for post in data:
            if ('attachments' in post.keys()) and post['attachments'][0]['type'] == 'photo':
                img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
            else:
                img_url = 'pass'

            pen.writerow((post['likes']['count'], post['text'], img_url))


group_domain = input()
posts = get_wall_posts(group_domain)
file_writer(posts)
