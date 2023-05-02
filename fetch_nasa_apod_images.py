import requests
import os
import argparse
from dotenv import load_dotenv, find_dotenv
from work_with_pic import download_pic, find_file_ext


def create_apod_pic_list(payload):
    url = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    apod_pics = response.json()
    return apod_pics


def fetch_apod_pic(apod_pics):
    url_pics = []
    for pic in apod_pics:
        if pic['url']:
            try:
                url_pics.append(pic['thumbnail_url'])
            except KeyError:
                url_pics.append(pic['url'])
        else:
            print(pic['date'], 'На эту дату нет фото')

    for count, pic in enumerate(url_pics):
        file_ext = find_file_ext(pic)
        filename = f'nasa_apod_{count}{file_ext}'
        download_pic(pic, filename)


def main():

    load_dotenv(find_dotenv())
    parser = argparse.ArgumentParser(
        description='Скачивает картинки с сервиса NASA APOD'
    )
    parser.add_argument('number_of_pic', help='Сколько картинок нужно скачать')
    args = parser.parse_args()
    nasa_api_key = os.environ['NASA_API_KEY']
    payload = {'api_key': nasa_api_key,
               'count': int(args.number_of_pic),
               'thumbs': True
               }
    apod_pics = create_apod_pic_list(payload)
    try:
        fetch_apod_pic(apod_pics)
        print('Все фото скачены')
    except ValueError:
        print('Вы ввели не число')


if __name__ == '__main__':
    main()
