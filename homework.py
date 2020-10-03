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
INIT_TIME_STAMP = int(time.time())

bot = telegram.Bot(token=TELEGRAM_TOKEN)


def parse_homework_status(homework: dict):
    if 'homework_name' not in homework or 'status' not in homework:
        raise Exception('An Error in function parse_homework_status '
                        f'with params homework={homework}')
    homework_name = homework.get('homework_name')
    status = homework.get('status')
    if status == 'approved':
        verdict = ('Ревьюеру всё понравилось, '
                   'можно приступать к следующему уроку.')
    else:
        verdict = 'К сожалению в работе нашлись ошибки.'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp: int):
    current_timestamp = current_timestamp if current_timestamp > 0 \
                        else INIT_TIME_STAMP
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    data = {'from_date': current_timestamp}
    url = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
    try:
        homework_statuses = requests.get(
                            url, headers=headers, params=data).json()
    except requests.exceptions.RequestException as e:
        logging.error(f'Some request\'s error: {e}')
        homework_statuses = {}
    return homework_statuses


def send_message(message: str):
    return bot.send_message(chat_id=CHAT_ID, text=message)


def main():
    current_timestamp = INIT_TIME_STAMP
    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(
                             new_homework.get('homeworks')[0]))
            new_homework.setdefault('current_date', INIT_TIME_STAMP)
            current_timestamp = new_homework.get('current_date')
            time.sleep(300)  # опрашивать раз в пять минут

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            logging.error(f'An Error Logging Message: {e}')
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()
