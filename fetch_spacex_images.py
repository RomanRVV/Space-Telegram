import requests
import argparse
from dotenv import load_dotenv, find_dotenv
from work_with_pic import download_pic


def fetch_spacex_last_launch(launch_id, path):
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    response = requests.get(url)
    response.raise_for_status()
    rocket_launch_pics = response.json()['links']['flickr']['original']
    if rocket_launch_pics:
        for count, pic in enumerate(rocket_launch_pics):
            filename = f'spacex{count}.jpg'
            download_pic(pic, filename, path)
        print('Все фото скачены')
    else:
        print('Фото на этом запуске не делали')


def main():
    load_dotenv(find_dotenv())
    parser = argparse.ArgumentParser(
        description='Скачивает картинки с запуска ракеты'
    )
    parser.add_argument('--launch_id', help='id запуска ракеты', default='latest')
    parser.add_argument('--path', help='В какую папку скачать картинки', default='images')
    args = parser.parse_args()
    fetch_spacex_last_launch(args.launch_id, args.path)


if __name__ == '__main__':
    main()
