import logging
import os
import tempfile

from telegram import Update
from telegram.ext import CallbackContext

from objects_detection.prediction import predict
from .types import CLASSES

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    logger.info(f'User {user.first_name} started the conversation.')

    update.message.reply_text(
        'Привет! Отправь изображение с товаром, и я подскажу актуальные цены в магазинах.'
    )


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


def image(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    chat_id = update.effective_chat.id
    image_file = update.message.photo[-1].get_file()

    tmp_directory = tempfile.TemporaryDirectory()
    try:
        image_path = os.path.join(tmp_directory.name, str(chat_id) + '.png')
        image_file.download(image_path)
        if not os.path.isfile(image_path):
            logger.error(f'Error while saving image {image_path}')
            return

        logger.info(f'Received image from {user.first_name}')

        update.message.reply_text(
            'Обработка...'
        )

        logger.info(f'Processing image {image_path}')
        label = predict(image_path)
        translation = CLASSES[label.lower()]

        update.message.reply_text(
            f'Здесь изображён {translation}, верно?'
        )
    except Exception as e:
        logger.error(f'Error in image processing {e}')
    finally:
        tmp_directory.cleanup()
