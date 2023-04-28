import os
from dotenv import load_dotenv, find_dotenv
import random
import time
import argparse
import telegram


def pic_list_create(pic_info_list):
    image_name_list = []
    for pic_info in pic_info_list:
        pic_name_list = pic_info[2]
        for pic_name in pic_name_list:
            image_name_list.append(pic_name)
    random.shuffle(image_name_list)
    return image_name_list


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
    pic_info_list = os.walk('images/')

    while True:
        for image in pic_list_create(pic_info_list):
            bot.sendDocument(chat_id=chat_id, document=open(f'images/{image}', 'rb'))
            time.sleep(args.time)


if __name__ == '__main__':
    main()
