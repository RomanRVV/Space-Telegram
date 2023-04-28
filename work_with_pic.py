import requests
from pathlib import Path
from os.path import split, splitext
from urllib.parse import urlsplit, unquote


def download_pic(url, filename):
    Path('images/').mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()

    with open(Path(f'images/{filename}'), 'wb') as file:
        file.write(response.content)
    return


def find_file_ext(url):
    url_tuple = urlsplit(url)
    path = unquote(url_tuple[2])
    file_name = split(path)[1]
    file_ext = splitext(file_name)[1]
    return file_ext
