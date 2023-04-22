import requests
import argparse
from dotenv import load_dotenv, find_dotenv
from work_with_pic import download_pic


def fetch_spacex_last_launch(launch_id):
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    response = requests.get(url)
    response.raise_for_status()
    rocket_launch_pic = response.json()['links']['flickr']['original']
    if rocket_launch_pic:
        for count, pic in enumerate(rocket_launch_pic):
            filename = f'spacex{count}.jpg'
            download_pic(pic, filename)
        print('Все фото скачены')
    else:
        print('Фото на этом запуске не делали')


def main():
    load_dotenv(find_dotenv())
    parser = argparse.ArgumentParser(
        description='Скачивает картинки с запуска ракеты'
    )
    parser.add_argument('--launch_id', help='id запуска ракеты')
    args = parser.parse_args()
    if args.launch_id:
        fetch_spacex_last_launch(args.launch_id)
    else:
        fetch_spacex_last_launch('latest')


if __name__ == '__main__':
    main()
