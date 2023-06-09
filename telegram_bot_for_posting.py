import os
from dotenv import load_dotenv, find_dotenv
import random
import time
import argparse
import telegram
from pathlib import Path


def create_image_for_posting(pics_info):
    images_name = [pic_name for pic_name in pics_info]
    random.shuffle(images_name)
    return images_name


def main():
    parser = argparse.ArgumentParser(
        description='Укажите раз в сколько секунд будет публиковаться картинка'
                    '(без указания аргумента задержка по умолчанию будет 4 часа)'
    )
    parser.add_argument('--time', help='Сколько секунд', type=int, default=14400)
    parser.add_argument('--path', help='Из какой папки брать картинки', default='images')
    args = parser.parse_args()
    load_dotenv(find_dotenv())
    tg_api_key = os.environ['TG_API_KEY']
    chat_id = os.environ['TG_CHAT_ID']
    bot = telegram.Bot(token=tg_api_key)
    pics_info = [pic for pic in Path(args.path).glob('*.*')]

    while True:
        for image in create_image_for_posting(pics_info):
            with open(Path(image), 'rb') as file:
                try:
                    bot.sendDocument(chat_id=chat_id, document=file)
                    time.sleep(args.time)
                except telegram.error.NetworkError:
                    time.sleep(10)


if __name__ == '__main__':
    main()
