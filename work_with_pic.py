import requests
from pathlib import Path
from os.path import split, splitext
from urllib.parse import urlsplit, unquote


def download_pic(url, filename, path):
    Path(f'{path}/').mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()

    with open(Path(f'{path}/{filename}'), 'wb') as file:
        file.write(response.content)


def find_file_ext(url):
    url_tuple = urlsplit(url)
    path_to_file = split(unquote(url_tuple.path))
    path_to_image, image_name = path_to_file
    image = splitext(image_name)
    name, ext = image
    return ext
