import logging
import os
import tempfile

from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from objects_detection.prediction import predict
from .utils import (get_keyboard, fetch_prices, format_content)
from .types import (CLASSES, READY, BUSY)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info(f'User {user.first_name} started the conversation.')

    update.message.reply_text(
        'Привет! Отправь изображение с товаром, и я подскажу актуальные цены в магазинах.'
    )

    return READY


def cancel(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    logger.info(f'User {user.first_name} canceled the conversation.')

    update.message.reply_text(
        f'Пока! Возвращайся, {user.first_name}!'
    )


def help_reply(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        f'Просто отправь изображение.'
    )


def image(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    chat_id = update.effective_chat.id
    image_file = update.message.photo[-1].get_file()

    tmp_directory = tempfile.TemporaryDirectory()
    try:
        image_path = os.path.join(tmp_directory.name, str(chat_id) + '.png')
        image_file.download(image_path)
        if not os.path.isfile(image_path):
            logger.error(f'Error while saving image {image_path}')
            return READY

        logger.info(f'Received image from {user.first_name}')

        update.message.reply_text(
            'Обработка...'
        )

        logger.info(f'Processing image {image_path}')
        label = predict(image_path)
        translation = CLASSES[label.lower()]

        context.user_data['product'] = translation

        update.message.reply_text(
            f'Здесь изображён {translation}, верно?',
            reply_markup=get_keyboard()
        )

        return BUSY
    except Exception as e:
        logger.error(f'Error in image processing {e}')
        return READY
    finally:
        tmp_directory.cleanup()


def clear_data(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    context.user_data.pop('product')

    query.edit_message_text(
        f'Давай попробуем другое изображение'
    )

    return READY


def prices(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    product = context.user_data.pop('product', None)

    if product is None:
        query.edit_message_text(
            f'Мне нечего искать'
        )
        return READY

    query.edit_message_text(
        f'Ищу цены...'
    )

    products = fetch_prices(product)
    formatted_text = format_content(products)

    query.edit_message_text(formatted_text)

    return READY
