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


def main():
    os.makedirs('files/', exist_ok=True)
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    r = response.json()
    image_url = r['img']
    image_name = get_image_name(image_url)
    image_download(image_url, f'files/{image_name}')


if __name__ == "__main__":
    main()