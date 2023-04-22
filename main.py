import requests
import os
import datetime
import argparse
from pathlib import Path
from os.path import split, splitext
from urllib.parse import urlsplit, unquote
from dotenv import load_dotenv, find_dotenv


def download_pic(url, path, filename):
    Path(path).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()

    with open(f'{path}{filename}', 'wb') as file:
        file.write(response.content)
    return


def fetch_spacex_last_launch(launch_id, path):
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    response = requests.get(url)
    response.raise_for_status()
    rocket_launch_pic = response.json()['links']['flickr']['original']

    for count, pic in enumerate(rocket_launch_pic):
        filename = f'spacex{count}.jpg'
        download_pic(pic, path, filename)


def find_file_ext(url):
    url_tuple = urlsplit(url)
    path = unquote(url_tuple[2])
    file_name = split(path)[1]
    file_ext = splitext(file_name)[1]
    return file_ext


def fetch_apod_pic(api_key, number_of_pic, path):
    payload = {'api_key': api_key,
               'count': number_of_pic,
               'thumbs': True
               }

    url = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    apod_pic = response.json()
    pic_list = []
    for pic in apod_pic:
        try:
            pic_list.append(pic['thumbnail_url'])
        except KeyError:
            pic_list.append(pic['url'])

    for count, pic in enumerate(pic_list):
        file_ext = find_file_ext(pic)
        filename = f'nasa_apod_{count}{file_ext}'
        download_pic(pic, path, filename)


def fetch_epic_pic(api_key, path, number_of_pic):
    pic_info_url = f'https://api.nasa.gov/EPIC/api/natural/available?api_key={api_key}'
    response = requests.get(pic_info_url)
    response.raise_for_status()

    pic_info = response.json()
    for count, pic in enumerate(pic_info[:number_of_pic]):
        aDate = datetime.date.fromisoformat(pic)
        formatted_date = aDate.strftime('%Y/%m/%d')
        url = f"https://api.nasa.gov/EPIC/api/natural/date/{aDate}?api_key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        try:
            download_pic_url = f'https://api.nasa.gov/EPIC/archive/natural/{formatted_date}/png/' \
                               f'{response.json()[0]["image"]}.png?api_key={api_key}'
            response = requests.get(download_pic_url)
            response.raise_for_status()
            filename = f'nasa_EPIC_{count}.png'
            download_pic(download_pic_url, path, filename)
        except IndexError:
            print('В сервисе EPIC отсутствует картинка на дату:', formatted_date)


def main():

    load_dotenv(find_dotenv())
    parser = argparse.ArgumentParser(
        description='Скачивает картинки с космической тематикой'
    )
    parser.add_argument('number_of_pic', help='Сколько картинок нужно скачать')
    parser.add_argument('path_to_pic', help='Путь до места сохранения картинок')
    args = parser.parse_args()
    NASA_API_KEY = os.environ['NASA_API_KEY']

    fetch_spacex_last_launch('5eb87d47ffd86e000604b38a', args.path_to_pic)
    fetch_apod_pic(NASA_API_KEY, int(args.number_of_pic), args.path_to_pic)
    fetch_epic_pic(NASA_API_KEY, args.path_to_pic, int(args.number_of_pic))


if __name__ == '__main__':
    main()
