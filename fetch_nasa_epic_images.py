import requests
import os
import datetime
import argparse
from dotenv import load_dotenv, find_dotenv
from work_with_pic import download_pic


def fetch_epic_pic(api_key, number_of_pic):
    payload = {'api_key': api_key}
    pic_info_url = f'https://api.nasa.gov/EPIC/api/natural/available'
    response = requests.get(pic_info_url, params=payload)
    response.raise_for_status()

    pic_info = response.json()
    for count, pic in enumerate(pic_info[(-number_of_pic-1):-1]):
        aDate = datetime.date.fromisoformat(pic)
        formatted_date = aDate.strftime('%Y/%m/%d')
        url = f"https://api.nasa.gov/EPIC/api/natural/date/{aDate}"
        response = requests.get(url, params=payload)
        response.raise_for_status()
        try:
            download_pic_url = f'https://api.nasa.gov/EPIC/archive/natural/{formatted_date}/png/' \
                               f'{response.json()[0]["image"]}.png'
            response = requests.get(download_pic_url, params=payload)
            response.raise_for_status()
            filename = f'nasa_EPIC_{count}.png'
            download_pic(response.url, filename)
        except IndexError:
            print('В сервисе EPIC отсутствует картинка на дату:', formatted_date)


def main():

    load_dotenv(find_dotenv())
    parser = argparse.ArgumentParser(
        description='Скачивает картинки с сервиса NASA EPIC'
    )
    parser.add_argument('number_of_pic', help='Сколько картинок нужно скачать')
    args = parser.parse_args()
    NASA_API_KEY = os.environ['NASA_API_KEY']
    try:
        fetch_epic_pic(NASA_API_KEY, int(args.number_of_pic))
        print('Все фото скачены')
    except ValueError:
        print('Вы ввели не число')


if __name__ == '__main__':
    main()
