import logging

from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    Filters,
    Updater
)

from .commands import (
    start,
    cancel,
    help_reply,
    image,
    clear_data,
    prices
)
from .types import READY, BUSY
from cfg.config import TOKEN

logger = logging.getLogger(__name__)


def get_bot() -> Updater:
    updater = Updater(token=TOKEN)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            READY: [
                MessageHandler(Filters.photo, image),
                MessageHandler(Filters.all, help_reply),
                CommandHandler('help', help_reply)
            ],
            BUSY: [
                CallbackQueryHandler(prices, pattern='^1$'),
                CallbackQueryHandler(clear_data, pattern='^2$')
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    updater.dispatcher.add_handler(conv_handler)
    logger.info('Bot has been configured')

    return updater
