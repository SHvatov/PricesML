import logging

from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    Filters,
    Updater
)

from .commands import (
    start,
    help_reply,
    image,
    clear_data,
    prices
)
from cfg.config import TOKEN

logger = logging.getLogger(__name__)


def get_bot() -> Updater:
    updater = Updater(token=TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, image))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, help_reply))
    updater.dispatcher.add_handler(CommandHandler('help', help_reply))
    updater.dispatcher.add_handler(CallbackQueryHandler(prices, pattern='^1$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(clear_data, pattern='^2$'))

    logger.info('Bot has been configured')

    return updater
