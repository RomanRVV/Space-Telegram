import os
from dotenv import load_dotenv, find_dotenv
import random
import time
import argparse
import telegram
from pathlib import Path


def create_image_for_posting(pics_info):
    images_name = []
    for pic_name in pics_info:
        images_name.append(pic_name)
    random.shuffle(images_name)
    return images_name


def main():
    parser = argparse.ArgumentParser(
        description='Укажите раз в сколько секунд будет публиковаться картинка'
                    '(без указания аргумента задержка по умолчанию будет 4 часа)'
    )
    parser.add_argument('--time', help='Сколько секунд', default=14400)
    args = parser.parse_args()
    load_dotenv(find_dotenv())
    tg_api_key = os.environ['TG_API_KEY']
    chat_id = os.environ['TG_CHAT_ID']
    bot = telegram.Bot(token=tg_api_key)
    pics_info = Path('images/').glob('*.*')

    while True:
        for image in create_image_for_posting(pics_info):
            with open(Path(image), 'rb') as file:
                bot.sendDocument(chat_id=chat_id, document=file)
                time.sleep(int(args.time))


if __name__ == '__main__':
    main()





