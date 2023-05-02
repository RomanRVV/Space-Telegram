import requests
import os
import datetime
import argparse
from dotenv import load_dotenv, find_dotenv
from work_with_pic import download_pic


def create_pic_info_list(payload):
    pic_info_url = f'https://api.nasa.gov/EPIC/api/natural/available'
    response = requests.get(pic_info_url, params=payload)
    response.raise_for_status()
    pic_info = response.json()
    return pic_info


def fetch_epic_pic(payload, pic, pic_number, path):
    a_date = datetime.date.fromisoformat(pic)
    formatted_date = a_date.strftime('%Y/%m/%d')
    url = f"https://api.nasa.gov/EPIC/api/natural/date/{a_date}"
    response = requests.get(url, params=payload)
    response.raise_for_status()
    pic_url_for_download = f'https://api.nasa.gov/EPIC/archive/natural/{formatted_date}/png/' \
                           f'{response.json()[0]["image"]}.png'
    filename = f'nasa_EPIC_{pic_number}.png'
    response = requests.get(pic_url_for_download, params=payload)
    try:
        response.raise_for_status()
        download_pic(response.url, filename, path)
    except IndexError:
        print('В сервисе EPIC отсутствует картинка на дату:', formatted_date)


def main():
    load_dotenv(find_dotenv())
    parser = argparse.ArgumentParser(
        description='Скачивает картинки с сервиса NASA EPIC'
    )
    parser.add_argument('number_of_pic', help='Сколько картинок нужно скачать')
    parser.add_argument('--path', help='В какую папку скачать картинки', default='images')
    args = parser.parse_args()
    nasa_api_key = os.environ['NASA_API_KEY']

    payload = {'api_key': nasa_api_key}
    pic_info = create_pic_info_list(payload)
    for count, pic in enumerate(pic_info[(-int(args.number_of_pic) - 1):-1]):
        try:
            fetch_epic_pic(payload, pic, count, args.path)
            print('Все фото скачены')
        except ValueError:
            print('Вы ввели не число')


if __name__ == '__main__':
    main()
