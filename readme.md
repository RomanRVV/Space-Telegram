# Скачивание и постниг картинок с космической тематикой 

Проект умеет скачивать фотографии с сервисов NASA APOD, NASA EPIC и SpaceX.

А после выкладывать их в телеграмм канал с заданной переодичностью.



### Как установить

Перейдите на сайт [NASA](https://api.nasa.gov/) и введите данные для генерации API-ключа.
Ключ придет на почту, которую Вы указали.


Пример ключа - `9XrvLxvH7I2gvsa1ssiYxbDxaGm2hzQbjhx4faBl`

Создайте файл .env и вставьте в него ключ.

`NASA_API_KEY = 9XrvLxvH7I2gvsa1ssiYxbDxaGm2hzQbjhx4faBl` 
(Что должно быть в файле .env )

Также необходимо внести в .env `telegram api key` и `telegram chat id`.
Подробная инструкция, как создать канал и телеграм бота 
[ссылка](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/)

`TG_API_KEY = 54124594394:AAHDpclK_EYq7yPrXszbcSnjO7QYdqgv5B4`
`TG_CHAT_ID = @test_test_tg`
(Что должно быть в файле .env )

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
### Примеры запуска скрипта

1 пример:
```
python fetch_spacex_images.py --launch_id 5eb87d47ffd86e000604b38a
```
Результат:
`Были скачены фотографии с сайта SpaceX, с конкретного запуска ракеты`

2 пример:
```
python fetch_nasa_apod_images.py 5
```
Результат:
`Скачивает 5 фотографий с сервиса NASA APOD`

3 пример:
```
python telegram_bot_for_posting.py --time 5
```
Результат:
`Постит картинки в телеграмм канал раз в 5 секунд`

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).