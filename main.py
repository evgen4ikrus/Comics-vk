from urllib import response
from dotenv import load_dotenv
import requests
from urllib.parse import unquote, urlparse
import os
from random import randint


def image_download(url, path):
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


def get_upload_url(vk_token, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': vk_token,
        'group_id': group_id,
        'v': 5.131,
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
    image = response.json()
    return image


def save_image_to_album(vk_token, vk_group_id, image):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token': vk_token,
        'group_id': vk_group_id,
        'server': image['server'],
        'photo': image['photo'],
        'hash': image['hash'],
        'v': 5.131,
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()


def post_image(vk_group_id, vk_token, image, message):
    url = 'https://api.vk.com/method/wall.post'
    owner_id = image['response'][0]['owner_id']
    media_id = image['response'][0]['id']
    
    params = {
        'access_token': vk_token,
        'v': 5.131,
        'owner_id': int(f'-{vk_group_id}'),
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
    
    os.makedirs('files/', exist_ok=True)
    comics_count = get_number_of_commics()
    comic = get_comic(randint(1, comics_count))
    comment = comic['alt']
    image_url = comic['img']
    image_name = get_image_name(image_url)
    
    image_download(image_url, f'files/{image_name}')
    upload_url = get_upload_url(vk_token, vk_group_id)
    image_path = f'files/{image_name}'
    image = upload_image_to_server(image_path, upload_url)
    comic = save_image_to_album(vk_token, vk_group_id, image)
    post_image(vk_group_id, vk_token, comic, comment)
    
    os.remove(image_path)

if __name__ == "__main__":
    main()