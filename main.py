from urllib import response
from dotenv import load_dotenv
import requests
from urllib.parse import unquote, urlparse
import os


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


def get_photo_upload_url(vk_token, group_id):
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


def main():
    os.makedirs('files/', exist_ok=True)
    url = 'https://xkcd.com/12/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic = response.json()
    comment = comic['alt']
    image_url = comic['img']
    image_name = get_image_name(image_url)
    image_download(image_url, f'files/{image_name}')
    
    
    load_dotenv()
    vk_group_id = os.getenv('VK_GROUP_ID')
    vk_token = os.getenv('VK_ACCESS_TOKEN')

    upload_url = get_photo_upload_url(vk_token, vk_group_id)
     

if __name__ == "__main__":
    main()