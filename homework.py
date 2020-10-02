import logging
import os
import time

from dotenv import load_dotenv

import requests

import telegram

load_dotenv()
logging.basicConfig(level=logging.INFO, filename='datacamp.log', filemode='w')

PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

bot = telegram.Bot(token=TELEGRAM_TOKEN)


def parse_homework_status(homework):
    homework.setdefault('homework_name', 'unknown work')
    homework.setdefault('status', '')
    homework_name = homework.get('homework_name')
    status = homework.get('status')
    if status == 'approved':
        verdict = ('Ревьюеру всё понравилось, '
                   'можно приступать к следующему уроку.')
    else:
        verdict = 'К сожалению в работе нашлись ошибки.'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    data = {'from_date': current_timestamp}
    url = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
    try:
        homework_statuses = requests.get(
                            url, headers=headers, params=data).json()
    except ConnectionError as e:
        logging.error(f'An Connection error in get_homework_statuses: {e}')
        homework_statuses = {}
    except Exception as e:
        logging.error(f'An error in get_homework_statuses: {e}')
        homework_statuses = {}
    return homework_statuses


def send_message(message):
    return bot.send_message(chat_id=CHAT_ID, text=message)


def main():
    current_timestamp = 0  # начальное значение timestamp
    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(
                             new_homework.get('homeworks')[0]))
            current_timestamp = new_homework.get('current_date')
            time.sleep(300)  # опрашивать раз в пять минут

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            logging.error(f'An Error Logging Message: {e}')
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()
