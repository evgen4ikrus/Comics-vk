from http import server
import os
from random import randint
import shutil
from urllib.parse import unquote, urlparse

import requests
from dotenv import load_dotenv


def download_image(url, path):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


def get_image_name(url):
    image_url = urlparse(url).path
    image_url = unquote(image_url, encoding='utf-8', errors='replace')
    image_name = os.path.split(image_url)[1]
    return image_name


def get_number_of_commics():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comics_count = response.json()['num']
    return comics_count


def get_comic(comic_number):
    url = f'https://xkcd.com/{comic_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic = response.json()
    return comic


def get_upload_url(vk_token, group_id, vk_api_version):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': vk_token,
        'group_id': group_id,
        'v': vk_api_version,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    upload_url = response.json()['response']['upload_url']
    return upload_url


def upload_image_to_server(path, upload_url):
    with open(path, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
    save_data = response.json()
    server = save_data['server']
    photo = save_data['photo']
    photo_hash = save_data['hash']
    return server, photo, photo_hash


def save_image_to_album(vk_token, vk_group_id,
                        vk_api_version, server, photo, hash):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token': vk_token,
        'group_id': vk_group_id,
        'server': server,
        'photo': photo,
        'hash': hash,
        'v': vk_api_version,
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()


def post_image(vk_group_id, vk_token, image, vk_api_version, message):
    url = 'https://api.vk.com/method/wall.post'
    owner_id = image['response'][0]['owner_id']
    media_id = image['response'][0]['id']

    params = {
        'access_token': vk_token,
        'v': vk_api_version,
        'owner_id': -int(vk_group_id),
        'attachments': f'photo{owner_id}_{media_id}',
        'from_group': 1,
        'message': message,
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()


def main():

    load_dotenv()

    vk_group_id = os.getenv('VK_GROUP_ID')
    vk_token = os.getenv('VK_ACCESS_TOKEN')
    vk_api_version = 5.131
    os.makedirs('files/', exist_ok=True)

    try:
        comics_count = get_number_of_commics()
        comic = get_comic(randint(1, comics_count))
        comment = comic['alt']
        image_url = comic['img']
        image_name = get_image_name(image_url)
        download_image(image_url, f'files/{image_name}')

        upload_url = get_upload_url(vk_token, vk_group_id, vk_api_version)
        image_path = f'files/{image_name}'
        server, photo, photo_hash = upload_image_to_server(image_path,
                                                           upload_url)
        comic = save_image_to_album(vk_token, vk_group_id, vk_api_version,
                                    server, photo, photo_hash)
        post_image(vk_group_id, vk_token, comic, vk_api_version, comment)

    finally:
        shutil.rmtree('files/')


if __name__ == "__main__":
    main()
