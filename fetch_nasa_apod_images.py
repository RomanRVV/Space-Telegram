import requests
import os
import argparse
from dotenv import load_dotenv, find_dotenv
from work_with_pic import download_pic, find_file_ext


def fetch_apod_pic(api_key, number_of_pic):
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
        if pic['url']:
            try:
                pic_list.append(pic['thumbnail_url'])
            except KeyError:
                pic_list.append(pic['url'])
        else:
            print(pic['date'], 'На эту дату нет фото')

    for count, pic in enumerate(pic_list):
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
    try:
        fetch_apod_pic(nasa_api_key, int(args.number_of_pic))
        print('Все фото скачены')
    except ValueError:
        print('Вы ввели не число')


if __name__ == '__main__':
    main()
