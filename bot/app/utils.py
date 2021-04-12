import json
import requests
import urllib.parse
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from cfg.config import API_URL, API_ENDPOINT


def get_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton('Да', callback_data='1'),
            InlineKeyboardButton('Нет', callback_data='2')
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def fetch_prices(product: str) -> list:
    url = urllib.parse.urljoin(API_URL, API_ENDPOINT)
    headers = {'Content-type': 'application/json'}
    payload = {
        'requestedProduct': product,
        'limit': 3,
        'requestFrom': 'LENTA'
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)

    return r.json()


def format_content(content: list) -> str:
    paragraphs = list()
    for el in content:
        paragraph = f'{el["title"]}\n' \
               f'Обычная цена:  {el["regularPrice"]}\n' \
               f'Цена со скидкой: {el["discountPrice"]}'
        paragraphs.append(paragraph)

    return '\n\n'.join(paragraphs)
